import asyncio
from typing import Dict, Set
from uuid import UUID

import zmq
import zmq.asyncio
from fastapi import WebSocket

from src.utils import SingletonMetaclass
from src.schemas import ComplexMessageSchema


class GatewayManager(metaclass=SingletonMetaclass):
    """
    Менеждер-синглтон соединений с TCP источниками и шлюзов из ZeroMQ в Websocket
    """

    # {complex_id: {websocket: {aliases}}}
    __websockets: Dict[UUID, Dict[WebSocket, Set[str]]]

    # {complex_id: task}
    __tasks: Dict[UUID, asyncio.Task]

    __context: zmq.asyncio.Context

    def __init__(self):
        self.__websockets = dict()
        self.__tasks = dict()
        self.__context = zmq.asyncio.Context()

    async def connect(
        self,
        complex_id: UUID,
        websocket: WebSocket,
        address: str,
        aliases: Set[str]
    ):
        if complex_id not in self.__websockets:
            self.__websockets[complex_id] = dict()
            task = asyncio.create_task(self._zmq_task(complex_id, address))
            self.__tasks[complex_id] = task

        self.__websockets[complex_id][websocket] = aliases

    async def disconnect(self, complex_id: UUID, websocket: WebSocket):
        if complex_id in self.__websockets:
            self.__websockets[complex_id].pop(websocket, None)

            if not self.__websockets[complex_id]:
                del self.__websockets[complex_id]
                if complex_id in self.__tasks:
                    self.__tasks[complex_id].cancel()
                    del self.__tasks[complex_id]

    async def _zmq_task(self, complex_id: UUID, address: str):
        zmq_socket = self.__context.socket(zmq.SUB)
        zmq_socket.setsockopt(zmq.SUBSCRIBE, b"")
        zmq_socket.setsockopt(zmq.RCVHWM, 1000)
        zmq_socket.connect(address)

        try:
            while True:
                message = await zmq_socket.recv()
                data = ComplexMessageSchema.model_validate_json(message)
                payload = data.poll_result.payload

                if payload and complex_id in self.__websockets:
                    broadcast_tasks = list()
                    for websocket, aliases in self.__websockets[complex_id].items():
                        payload_aliases = set([item.name for item in payload])
                        common_aliases = aliases & payload_aliases
                        
                        if common_aliases:
                            filtered_payload = {
                                item.name: item.value
                                for item in payload
                                if item.name in common_aliases
                            }
                            broadcast_tasks.append(websocket.send_json(filtered_payload))
                    
                    if broadcast_tasks:
                        await asyncio.gather(*broadcast_tasks, return_exceptions=True)
                            

        except asyncio.CancelledError:
            print(f"ZMQ listener for complex '{complex_id.hex[:8]}' stopped.")
        finally:
            zmq_socket.close()

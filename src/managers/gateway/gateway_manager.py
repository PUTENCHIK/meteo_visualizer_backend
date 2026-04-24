import asyncio
import zmq
import zmq.asyncio
from uuid import UUID
from fastapi import WebSocket
from typing import Dict, Set
from src.utils import SingletonMetaclass


class GatewayManager(metaclass=SingletonMetaclass):
    """
    Менеждер-синглтон соединений с TCP источниками и шлюзов из ZeroMQ в Websocket
    """

    __websockets: Dict[UUID, Set[WebSocket]]

    __tasks: Dict[UUID, asyncio.Task]

    __context: zmq.asyncio.Context

    def __init__(self):
        self.__websockets = dict()
        self.__tasks = dict()
        self.__context = zmq.asyncio.Context()
    
    async def connect(self, complex_id: UUID, websocket: WebSocket, address: str):
        if complex_id not in self.__websockets:
            self.__websockets[complex_id] = set()
            task = asyncio.create_task(self._zmq_task(complex_id, address))
            self.__tasks[complex_id] = task
            
        self.__websockets[complex_id].add(websocket)

    async def disconnect(self, complex_id: UUID, websocket: WebSocket):
        if complex_id in self.__websockets:
            self.__websockets[complex_id].remove(websocket)
            
            if not self.__websockets[complex_id]:
                del self.__websockets[complex_id]
                if complex_id in self.__tasks:
                    self.__tasks[complex_id].cancel()
                    del self.__tasks[complex_id]

    async def _zmq_task(self, complex_id: UUID, address: str):
        zmq_socket = self.__context.socket(zmq.SUB)
        zmq_socket.setsockopt(zmq.SUBSCRIBE, b"")
        zmq_socket.connect(address)
        
        try:
            while True:
                message = await zmq_socket.recv()
                
                if complex_id in self.__websockets:
                    broadcast_tasks = [
                        ws.send_text(message.decode("utf-8")) 
                        for ws in self.__websockets[complex_id]
                    ]
                    await asyncio.gather(*broadcast_tasks, return_exceptions=True)
                    
        except asyncio.CancelledError:
            print(f"ZMQ listener for complex '{complex_id.hex[:8]}' stopped.")
        finally:
            zmq_socket.close()

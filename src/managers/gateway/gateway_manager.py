import asyncio
from typing import Dict, Set
from uuid import UUID

import zmq
import zmq.asyncio
from fastapi import WebSocket

from src.schemas import (
    ComplexMessageSchema,
    ComplexWithMastsSchema,
    MessagePayloadSchema,
)
from src.utils import SingletonMetaclass
from src.utils.exceptions import ComplexHasNoAddressException
from src.utils.parser import WeatherDeviceParser


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
        complex: ComplexWithMastsSchema,
        websocket: WebSocket,
        aliases: Set[str]
    ):
        if not complex.address:
            raise ComplexHasNoAddressException(complex.id)

        if complex.id not in self.__websockets:
            self.__websockets[complex.id] = dict()
            task = asyncio.create_task(self._zmq_task(complex))
            self.__tasks[complex.id] = task

        self.__websockets[complex.id][websocket] = aliases

    async def disconnect(self, complex_id: UUID, websocket: WebSocket):
        if complex_id in self.__websockets:
            self.__websockets[complex_id].pop(websocket, None)

            if not self.__websockets[complex_id]:
                del self.__websockets[complex_id]
                if complex_id in self.__tasks:
                    self.__tasks[complex_id].cancel()
                    del self.__tasks[complex_id]

    async def _zmq_task(self, complex: ComplexWithMastsSchema):
        zmq_socket = self.__context.socket(zmq.SUB)
        zmq_socket.setsockopt(zmq.SUBSCRIBE, b"")
        zmq_socket.setsockopt(zmq.RCVHWM, 1000)
        zmq_socket.connect(complex.address)

        try:
            while True:
                message = await zmq_socket.recv()
                await self._process_zmq_message(message, complex)

        except asyncio.CancelledError:
            print(f"ZMQ listener for complex '{complex.id.hex[:8]}' stopped.")
        except Exception as e:
            print(f"Exception in task {complex.id.hex[:8]}: {e}")
        finally:
            zmq_socket.close(linger=0)
            await self._internal_cleanup(complex.id)
        
    async def _process_zmq_message(
        self,
        message: bytes,
        complex: ComplexWithMastsSchema
    ):
        try:
            data = ComplexMessageSchema.model_validate_json(message)
            payload = data.poll_result.payload

            if payload is None or complex.id not in self.__websockets:
                return
            
            broadcast_tasks = list()
            device_name = WeatherDeviceParser.parse_name(
                data.pollable_name
            )
            mast = next((
                mast
                for mast in complex.masts
                if mast.prefix.lower() == device_name.mast.lower()
            ), None)
            if mast is None or mast.config is None:
                return
            
            yard = None
            for i, y in enumerate(mast.config.yards):
                if i+1 == device_name.yard:
                    yard = y
            if yard is None:
                return
            
            if device_name.num > yard.amount:
                return
            
            for websocket, aliases in self.__websockets[complex.id].items():
                payload_aliases = set([item.name for item in payload])
                common_aliases = aliases & payload_aliases
                
                if common_aliases:
                    items = [
                        item
                        for item in payload
                        if item.name in common_aliases
                    ]
                    schema = MessagePayloadSchema(
                        pollable_name=data.pollable_name,
                        device_name=device_name,
                        timestamp=data.poll_result.timestamp,
                        items=items,
                    )
                    broadcast_tasks.append(websocket.send_json(schema.model_dump()))
            
            if broadcast_tasks:
                await asyncio.gather(*broadcast_tasks, return_exceptions=True)    
        except Exception:
            pass
    
    async def _internal_cleanup(self, complex_id: UUID):
        websockets = self.__websockets.pop(complex_id, {})
        for ws in websockets:
            try:
                await ws.close(code=1001)
            except Exception:
                pass
            
        self.__tasks.pop(complex_id, None)
            

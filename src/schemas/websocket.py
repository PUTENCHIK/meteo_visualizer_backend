from enum import Enum
from typing import List, Optional

from src.schemas.base import BaseSchema


class PayloadItem(BaseSchema):
    description: str
    name: str
    units: str
    value: float


class PollStatus(Enum):
    DONE = "DONE"
    ERROR = "ERROR"
    DEACTIVATED = "DEACTIVATED"
    CONNECTION_FAILURE = "CONNECTION FAILURE"


class DebugInfo(BaseSchema):
    poll_start_time: float
    poll_end_time: float

    class Meta:
        field_numpy_dtype_map = {
            "poll_start_time": "i8",
            "poll_end_time": "i8",
        }


class PollResult(BaseSchema):
    timestamp: float
    payload: Optional[List[PayloadItem]] = None
    status: PollStatus = PollStatus.DONE
    debug_info: Optional[DebugInfo] = None


class ComplexMessageSchema(BaseSchema):
    pollable_name: str
    pipelines: Optional[List[str]] = []
    poll_result: PollResult = None

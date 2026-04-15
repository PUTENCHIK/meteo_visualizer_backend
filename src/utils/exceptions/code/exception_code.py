from enum import Enum, auto


class ExceptionCode(Enum):
    INTERNAL_ERROR = auto()
    INVALID_CREDENTIALS = auto()
    TOKEN_EXPIRED = auto()
    TOKEN_INVALID = auto()
    HTTP_ERROR = auto()
    VALIDATION = auto()

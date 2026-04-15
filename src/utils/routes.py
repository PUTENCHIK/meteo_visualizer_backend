from typing import Any, Dict, List

from fastapi.responses import JSONResponse

from src.schemas import ErrorResponse, ResponseModel
from src.utils.exceptions import ExceptionCode

DEFAULT_RESPONSES: List[ResponseModel] = [
    ResponseModel(status_code=500, description="Внутренняя ошибка сервера"),
]

AUTH_RESPONSES: List[ResponseModel] = [
    ResponseModel(status_code=401, description="Не авторизован"),
    ResponseModel(status_code=403, description="Доступ запрещен"),
]


def get_responses(
    responses: List[ResponseModel] = None, include_auth: bool = True
) -> Dict[int | str, Dict[str, Any]]:
    result = DEFAULT_RESPONSES[:]
    if include_auth:
        result.extend(AUTH_RESPONSES)
    if responses is not None:
        result.extend(responses)

    return {
        resp.status_code: {"model": ErrorResponse, "description": resp.description}
        for resp in result
    }


def create_error_response(status_code: int, code: ExceptionCode, message: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": {
                "code": code.name,
                "message": message,
            }
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

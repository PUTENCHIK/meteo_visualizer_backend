from typing import Any, Dict, List

from src.schemas import ErrorResponse, ResponseModel

DEFAULT_RESPONSES: List[ResponseModel] = [
    ResponseModel(status_code=401, description="Не авторизован"),
    ResponseModel(status_code=403, description="Доступ запрещен"),
    ResponseModel(status_code=500, description="Внутренняя ошибка сервера"),
]


def default_responses(
    responses: List[ResponseModel] = None,
) -> Dict[int | str, Dict[str, Any]]:
    result = DEFAULT_RESPONSES
    if responses is not None:
        result += responses

    return {
        resp.status_code: {"model": ErrorResponse, "description": resp.description}
        for resp in result
    }

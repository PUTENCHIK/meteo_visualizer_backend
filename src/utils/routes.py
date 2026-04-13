from typing import Any, Dict, List

from src.schemas import ErrorResponse, ResponseModel

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

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


class ResponseModel(BaseModel):
    status_code: int
    description: str

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    details: str


class ResponseModel(BaseModel):
    status_code: int
    description: str

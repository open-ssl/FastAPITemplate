from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: int
    data: str
    details: str

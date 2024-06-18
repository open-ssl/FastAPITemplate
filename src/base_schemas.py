from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: int
    type: str

from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: str
    data: str
    details: str


BaseResponseOK = {
    "status": "Success",
    "data": "",
    "details": "",
}

BaseResponseFailed = {
    "status": "Failed",
    "data": "",
    "details": "",
}

BaseResponseError = {
    "status": "Error",
    "data": "",
    "details": "",
}

BaseResponseServerError = {
    "status": "Error",
    "data": "Something went wrong during your request."
    "We are already working on this problem",
    "details": "",
}

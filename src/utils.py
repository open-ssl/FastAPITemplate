from fastapi import Request, HTTPException
from http import HTTPStatus


class Paginator:
    def __init__(self, offset: int = 0, limit: int = 10):
        self.offset = offset
        self.limit = limit

    def as_dict(self):
        return {"limit": self.limit, "offset": self.offset}


class AuthHealthChecker:
    def __init__(self, app_name):
        self.name = app_name
        self.params = []

    def __call__(self, request: Request):
        if "approved_cookie" not in request.cookies.keys():
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="No access")

        # todo Check data in cookies
        return self


auth_guard = AuthHealthChecker("FastAPI Template")

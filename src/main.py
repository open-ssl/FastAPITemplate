import time

from fastapi import FastAPI, Depends, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from redis import asyncio as aioredis

from src.auth.base_config import auth_backend, fastapi_users, current_user
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.config import REDIS_HOST, REDIS_PORT
from src.database import get_async_session
from src.utils import auth_guard, Paginator

from src.operations.router import router as operation_router
from src.tasks.router import router as tasks_router
from src.pages.router import router as pages_router
from src.ws_chat.router import router as chat_router

app = FastAPI(title="Template App")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
    dependencies=[],
)

app.include_router(operation_router)
app.include_router(tasks_router)
app.include_router(pages_router)
app.include_router(chat_router)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/unprotected-route")
def unprotected_route():
    return "Hello, Annonymus"


@app.get("/session")
async def get_session(_=Depends(get_async_session)):
    return


@app.get("/pagination_params")
async def get_params(params: Paginator = Depends(Paginator)):
    return params


@app.get("/guard_params", dependencies=[Depends(auth_guard)])
async def get_guard_params():
    return auth_guard.params


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        f"redis://localhost:{REDIS_PORT}", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

# Use right redirect to HTTPS or WS
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
# app.add_middleware(HTTPSRedirectMiddleware)


@app.middleware("http")
async def process_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{round(process_time, 6)} seconds"
    return response


# FOR Debug mode ONLY. It shows server's error to user
async def validation_exception_handler(_: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


#
# some_users_data_in_memory = list(
#     [
#         {"id": 1, "role": "admin", "name": "Stas 1"},
#         {"id": 2, "role": "investor", "name": "Stas 2"},
#         {"id": 3, "role": "trader", "name": "Stas 3"},
#         {
#             "id": 4,
#             "role": "trader",
#             "name": "Stas 3",
#             "degree": [{"id": 1, "created_at": "2021-01-01", "type_degree": "expert"}],
#         },
#     ]
# )
#
# some_trades_data_in_memory = list(
#     [
#         {
#             "id": 1,
#             "user_id": 1,
#             "currency": "BTC",
#             "side": "buy",
#             "price": 123,
#             "amount": 2.12,
#         },
#         {
#             "id": 2,
#             "user_id": 1,
#             "currency": "BTC",
#             "side": "sell",
#             "price": 125,
#             "amount": 2.12,
#         },
#         {
#             "id": 3,
#             "user_id": 1,
#             "currency": "BTC",
#             "side": "buy",
#             "price": 130,
#             "amount": 5,
#         },
#     ]
# )
#
#
# class DegreeType(Enum):
#     newbie = "newbie"
#     expert = "expert"
#
#
# class Degree(BaseModel):
#     id: int
#     created_at: datetime
#     type_degree: DegreeType
#
#
# class User(BaseModel):
#     id: int
#     role: str
#     name: str
#     degree: Optional[List[Degree]] = []
#
#
# @app.get("/users/{user_id}", response_model=List[User])
# def get_user(user_id: int):
#     return [user for user in some_users_data_in_memory if user_id == user.get("id")]
#
#
# @app.post("/users/{user_id}")
# def change_user_name(user_id: int, new_user_name: str):
#     current_user_data = list(
#         filter(lambda user: user.get("id") == user_id, some_users_data_in_memory)
#     )
#
#     if not current_user_data:
#         return dict({"status": 404})
#
#     current_user = current_user_data[0]
#     current_user["name"] = new_user_name
#     return dict({"status": 200, "data": current_user})
#
#
# @app.get("/trades")
# def get_trades(limit: int = 1, offset: int = 0):
#     return some_trades_data_in_memory[offset:][:limit]
#
#
# class Trade(BaseModel):
#     id: int
#     user_id: int
#     currency: str = Field(max_length=5)
#     side: str
#     price: float = Field(ge=0)
#     amount: float
#
#
# @app.post("/trades")
# def add_trades(trades: List[Trade]):
#     some_trades_data_in_memory.append(trades)
#     return {"status": 200, "data": some_trades_data_in_memory}


if __name__ == "__main__":
    app.mount("/static", StaticFiles(directory="./src/static"), name="static")
    app.add_exception_handler(
        exc_class_or_status_code=ValidationError, handler=validation_exception_handler
    )

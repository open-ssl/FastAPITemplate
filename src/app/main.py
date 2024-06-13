from datetime import datetime
from enum import Enum

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError

app = FastAPI(title="Template App")


# ONLY FOR Debug mode. Show server error to user
@app.exception_handler(ValidationError)
async def validation_exception_handler(_: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


some_users_data_in_memory = list(
    [
        {"id": 1, "role": "admin", "name": "Stas 1"},
        {"id": 2, "role": "investor", "name": "Stas 2"},
        {"id": 3, "role": "trader", "name": "Stas 3"},
        {
            "id": 4,
            "role": "trader",
            "name": "Stas 3",
            "degree": [{"id": 1, "created_at": "2021-01-01", "type_degree": "expert"}],
        },
    ]
)

some_trades_data_in_memory = list(
    [
        {
            "id": 1,
            "user_id": 1,
            "currency": "BTC",
            "side": "buy",
            "price": 123,
            "amount": 2.12,
        },
        {
            "id": 2,
            "user_id": 1,
            "currency": "BTC",
            "side": "sell",
            "price": 125,
            "amount": 2.12,
        },
        {
            "id": 3,
            "user_id": 1,
            "currency": "BTC",
            "side": "buy",
            "price": 130,
            "amount": 5,
        },
    ]
)


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in some_users_data_in_memory if user_id == user.get("id")]


@app.post("/users/{user_id}")
def change_user_name(user_id: int, new_user_name: str):
    current_user_data = list(
        filter(lambda user: user.get("id") == user_id, some_users_data_in_memory)
    )

    if not current_user_data:
        return dict({"status": 404})

    current_user = current_user_data[0]
    current_user["name"] = new_user_name
    return dict({"status": 200, "data": current_user})


@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return some_trades_data_in_memory[offset:][:limit]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades")
def add_trades(trades: List[Trade]):
    some_trades_data_in_memory.append(trades)
    return {"status": 200, "data": some_trades_data_in_memory}

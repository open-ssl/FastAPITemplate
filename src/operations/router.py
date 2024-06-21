import http
import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.base_schemas import (
    BaseResponse,
    BaseResponseOK,
    BaseResponseFailed,
    BaseResponseServerError,
)
from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationRead, OperationCreate

router = APIRouter(prefix="/operations", tags=["Operations"])


@router.get("/long_operation")
@cache(expire=30)
def get_long_operation():
    time.sleep(2)
    return "Some usefull info!"


@router.get("/")  # , response_model=List[OperationRead]
async def get_specific_operations(
    operation_type: str, session: AsyncSession = Depends(get_async_session)
):
    try:
        query = (
            select(operation)
            .where(operation.c.type == operation_type)
            .order_by(operation.c.id)
            .limit(10)
        )
        result = await session.execute(query)
        if not result:
            return []

        response = BaseResponseOK
        response["data"] = result.mappings().all()
        return response
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "data": None,
                "details": None,
            },
        )


@router.post("/", response_model=BaseResponse)
async def add_specific_operations(
    input_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(operation).values(**input_operation.dict())
    try:
        await session.execute(stmt)
        await session.commit()
    except IntegrityError:
        response_details = BaseResponseFailed
        response_details["data"] = "Duplicate error"
        response_details["details"] = (
            "You are trying to add duplicate record. Change request params "
            "and try again. "
        )

        raise HTTPException(
            status_code=http.HTTPStatus.CONFLICT,
            detail=response_details,
        )
    except Exception:
        raise HTTPException(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=BaseResponseServerError,
        )

    return BaseResponseOK

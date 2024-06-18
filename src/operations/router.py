from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.base_schemas import BaseResponse
from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationRead, OperationCreate

router = APIRouter(prefix="/operations", tags=["Operation"])


@router.get("/") # , response_model=List[OperationRead]
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type).order_by(operation.c.id).limit(10)
        result = await session.execute(query)
        if not result:
            return []

        return {
            "status": "success",
            "data":  result.mappings().all(),
            "details": None,
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None,
        })


@router.post("/", response_model=BaseResponse)
async def add_specific_operations(input_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    statement = insert(operation).values(**input_operation.dict())
    await session.execute(statement)
    await session.commit()
    return {"status": 200, "type": "Success"}

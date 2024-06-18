from fastapi import APIRouter

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]

)


@router.get("/")
async def get_operations():
    return "No operations at the moment"

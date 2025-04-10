from fastapi import Depends
from fastapi import APIRouter
from infra.mysql import get_mysql_session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.order import OrderFilterRequest


router = APIRouter()


@router.post("/filter")
async def get_order_filter(
        # req: OrderFilterRequest,
        db: AsyncSession = Depends(get_mysql_session)):

    return {"message": f"This is [post] /order/filter"}

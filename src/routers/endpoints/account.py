from fastapi import Depends
from fastapi import APIRouter
from infra.mysql import get_mysql_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/{account_id}/order")
async def get_account_orders(
        account_id,
        db: AsyncSession = Depends(get_mysql_session)):

    return {"message": f"This is [get] /account/{account_id}/order"}


@router.get("/{account_id}/message")
async def get_account_messages(
        account_id,
        db: AsyncSession = Depends(get_mysql_session)):

    return {"message": f"This is [get] /account/{account_id}/message"}

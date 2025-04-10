from fastapi import Depends
from fastapi import APIRouter
from infra.mysql import get_mysql_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.account import Account
from models.order import Order
from models.message import Message
from models.message_log import MessageLog


router = APIRouter()


@router.get("/{account_id}/order")
async def get_account_orders(
        account_id,
        db: AsyncSession = Depends(get_mysql_session)):

    result = await db.execute(
        select(Order)
        .where(Order.account_id == account_id)
        .order_by(Order.created_at.desc())
    )

    raw_orders = result.scalars().all()
    orders = []

    for order in raw_orders:
        data = order.as_dict()
        data.pop("account_id")
        data.pop("updated_at")
        orders.append(data)

    return orders


@router.get("/{account_id}/message")
async def get_account_messages(
        account_id,
        db: AsyncSession = Depends(get_mysql_session)):

    result = await db.execute(
        select(MessageLog.id, MessageLog.created_at)
        .join(Message, MessageLog.message_id == Message.id)
        .where(MessageLog.account_id == account_id)
        .order_by(MessageLog.created_at.desc())
    )

    return result.all()

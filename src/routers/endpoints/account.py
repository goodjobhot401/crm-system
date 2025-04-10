from fastapi import Depends
from fastapi import APIRouter
from infra.mysql import get_mysql_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.account import Account
from models.order import Order
from models.message_log import MessageLog


router = APIRouter()


@router.get("/all")
async def get_accounts(
        db: AsyncSession = Depends(get_mysql_session)):

    result = await db.execute(
        select(Account)
    )

    raw_accounts = result.scalars().all()
    accounts = []
    if raw_accounts:
        for account in raw_accounts:
            data = account.as_dict()
            data.pop("updated_at")
            accounts.append(data)

    return accounts


@router.get("/{id}/order")
async def get_account_orders(
        id,
        db: AsyncSession = Depends(get_mysql_session)):

    result = await db.execute(
        select(Order)
        .where(Order.account_id == id)
        .order_by(Order.created_at.desc())
    )

    raw_orders = result.scalars().all()
    if raw_orders:
        orders = []

        for order in raw_orders:
            data = order.as_dict()
            data.pop("account_id")
            data.pop("updated_at")
            orders.append(data)

        return orders
    return []


@router.get("/{id}/message")
async def get_account_messages(
        id,
        db: AsyncSession = Depends(get_mysql_session)):

    result = await db.execute(
        select(MessageLog)
        .where(MessageLog.account_id == id)
        .order_by(MessageLog.created_at.desc())
    )

    raw_messages = result.scalars().all()
    if raw_messages:
        messages = []

        for message in raw_messages:
            data = message.as_dict()
            data.pop("account_id")
            data.pop("message_id")
            data.pop("updated_at")
            messages.append(data)

        return messages

    return []

import json
from fastapi import Depends
from fastapi import APIRouter
from infra.mysql import get_mysql_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.message import Message
from models.message_log import MessageLog
from schemas.message import SendMessagesRequest


router = APIRouter()


@router.get("/templates")
async def get_messages(
        db: AsyncSession = Depends(get_mysql_session)):

    result = await db.execute(
        select(Message)
    )

    raw_templates = result.scalars().all()
    templates = []

    for template in raw_templates:
        data = template.as_dict()
        data.pop("updated_at")
        templates.append(data)

    return templates


async def send(messages):
    for message in messages:
        print(message)

"""
{
    "message_id": 1,
    "send_list": [
        {
            "account_id": 1,
            "name": "test_user_1",
            "amount": 10000
        },
        {
            "account_id": 2,
            "name": "test_user_2",
            "amount": 40000
        }
    ]
}

"""


@router.post("/send")
async def send_messages(
        req: SendMessagesRequest,
        db: AsyncSession = Depends(get_mysql_session)):

    account_list = req.send_list
    message_id = req.message_id

    template_result = await db.execute(
        select(Message)
        .where(Message.id == message_id)
    )
    raw_template = template_result.scalar_one_or_none()
    if not raw_template:
        return {"message": f"message_id: {message_id} not found"}

    title = raw_template.title
    template = raw_template.template

    messages = []
    logs = []
    for account in account_list:
        text = template.format(name=account.name, amount=account.amount)
        content = f"【{title}】\n{text}"

        logs.append((account.account_id, message_id, content))
        messages.append({"message": content})

    message_logs = [MessageLog(
        account_id=log[0],
        message_id=log[1],
        content=log[2]
    ) for log in logs]

    db.add_all(message_logs)
    await db.flush()
    await db.commit()
    await send(messages)
    return messages


@router.get("/{message_log_id}")
async def get_message_log_by_id(
        message_log_id,
        db: AsyncSession = Depends(get_mysql_session)):

    result = await db.execute(
        select(MessageLog)
        .where(MessageLog.id == message_log_id)
    )

    raw_message_log = result.scalar_one_or_none()
    if not raw_message_log:
        return {"message": "message_log_id not found"}

    message_log = raw_message_log.as_dict()
    return message_log

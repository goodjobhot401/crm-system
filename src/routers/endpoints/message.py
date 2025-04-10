from fastapi import Depends
from fastapi import APIRouter
from infra.mysql import get_mysql_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get("/all")
async def get_messages(
        db: AsyncSession = Depends(get_mysql_session)):

    return {"message": f"This is [get] /message/all"}


@router.post("/send")
async def send_messages(
        db: AsyncSession = Depends(get_mysql_session)):

    return {"message": f"This is [post] /message/send"}


@router.get("/{message_id}")
async def get_message_by_id(
        message_id,
        db: AsyncSession = Depends(get_mysql_session)):

    return {"message": f"This is [get] /message/{message_id}"}

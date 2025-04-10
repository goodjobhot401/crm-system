from datetime import datetime
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, TIMESTAMP, Text, func


class MessageLog(Base):
    __tablename__ = "message_log"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("account.id"))
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("message.id"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    account = relationship("Account")
    message = relationship("Message")

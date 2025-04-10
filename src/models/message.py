from datetime import datetime
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, TIMESTAMP, String, Text, func


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    template: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

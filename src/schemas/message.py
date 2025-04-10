from pydantic import BaseModel
from typing import List


class Account(BaseModel):
    account_id: int
    name: str
    amount: int


class SendMessagesRequest(BaseModel):
    message_id: int
    send_list: List[Account]

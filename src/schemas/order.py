from pydantic import BaseModel, Field
from typing import Optional, Literal
from decimal import Decimal
from datetime import datetime


class DateFilter(BaseModel):
    filter_type: Literal["between", "before", "after", "last_n_days"]
    from_date: Optional[datetime] = Field(
        None, description="Required if filter_type is 'between', ISO datetime string")
    to_date: Optional[datetime] = Field(
        None, description="Required if filter_type is 'between', ISO datetime string")
    before_date: Optional[datetime] = Field(
        None, description="Required if filter_type is 'before', ISO datetime string")
    after_date: Optional[datetime] = Field(
        None, description="Required if filter_type is 'after', ISO datetime string")
    days: Optional[int] = Field(
        None, description="Required if filter_type is 'last_n_days'"
    )


class AmountFilter(BaseModel):
    filter_type: Literal["between", "gte", "lte"]
    amount: Optional[Decimal] = Field(
        None, description="Required if filter_type is 'gte' or 'lte'"
    )
    min_value: Optional[Decimal] = Field(
        None, description="Required if filter_type is 'between'"
    )
    max_value: Optional[Decimal] = Field(
        None, description="Required if filter_type is 'between'"
    )


class OrderFilterRequest(BaseModel):
    date_filter: DateFilter
    amount_filter: AmountFilter

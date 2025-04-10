from pydantic import BaseModel, Field
from typing import Optional, Literal
from decimal import Decimal


class DateFilter(BaseModel):
    filter_type: Literal["between", "before", "after", "last_n_days"]
    from_day: Optional[int] = Field(None, description="Unix timestamp")
    to_day: Optional[int] = Field(None, description="Unix timestamp")
    days: Optional[int] = None


class AmountFilter(BaseModel):
    filter_type: Literal["between", "gte", "lte"]
    amount: Optional[Decimal] = None
    min_value: Optional[Decimal] = None
    max_value: Optional[Decimal] = None


class OrderFilterRequest(BaseModel):
    date_filter: DateFilter
    amount_filter: AmountFilter

from fastapi import Depends
from fastapi import APIRouter
from datetime import datetime, timedelta
from infra.mysql import get_mysql_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy import select, func
from schemas.order import OrderFilterRequest
from models.order import Order
from models.account import Account


router = APIRouter()


"""
example
// 在 '指定日期區間' '金額區間' 
{
    "date_filter": {
        "filter_type": "between",
        "from_date": "2022-04-11T00:00:00", 
        "to_date": "2025-04-11T23:59:59"
    },
    "amount_filter": {
        "filter_type": "between",
        "min_value": 10000,
        "max_value": 20000
    }
}

// 在 '指定日期之後' '金額區間' 
{
    "date_filter": {
        "filter_type": "after",
        "after_date": "2022-12-11T00:00:00"
    },
    "amount_filter": {
        "filter_type": "between",
        "min_value": 20000,
        "max_value": 500000
    }
}

// 在 '近幾日' '金額高於'
{
    "date_filter": {
        "filter_type": "last_n_days",
        "days": 200
    },
    "amount_filter": {
        "filter_type": "gte",
        "amount": 100 
    }
}


// 在 '近幾日' '金額低於'
{
    "date_filter": {
        "filter_type": "last_n_days",
        "days": 200
    },
    "amount_filter": {
        "filter_type": "lte",
        "amount": 20000 
    }
}
"""


@router.post("/filter")
async def get_order_filter(
        req: OrderFilterRequest,
        db: AsyncSession = Depends(get_mysql_session)):
    """
        根據指定的 '時間' 與 '金額' 條件篩選客戶群，整理成 list 回傳

        request body: OrderFilterRequest 由兩個欄位組成
        - 'date_filter' 處理訂單的時間條件
            filter_type 可為
            - 'between'：介於 'from_date' ~ 'to_date'
            - 'before'：早於指定日期 'before_date'
            - 'after'：晚於指定日期 'after_date'
            - 'last_n_days'：過去 N 天內, 'days' 為整數

        - 'amount_filter' 處理消費金額條件
            filter_type 可為
            - 'between'：介於 'min_value' ~ 'max_value'
            - 'gte'：大於等於 'amount'
            - 'lte'：小於等於 'amount'

        查詢邏輯
            - 根據 '時間' 條件篩出客戶群資料
            - 以 'account' 為組別算出每組的 'total_amout'
            - 再依照 'total_amout' 篩選出符合 '金額' 條件的客戶群
    """

    AccountAlias = aliased(Account)

    query = select(
        AccountAlias.id,
        AccountAlias.name,
        func.sum(Order.amount).label("total_amount")
    ).join(AccountAlias, AccountAlias.id == Order.account_id
           ).group_by(AccountAlias.id, AccountAlias.name)

    d_filter = req.date_filter
    d_type = d_filter.filter_type
    if d_type == "between" and d_filter.from_date and d_filter.to_date:
        query = query.where(Order.created_at.between(
            d_filter.from_date, d_filter.to_date))
    elif d_type == "last_n_day" and d_filter.days:
        ago = datetime.now() - timedelta(days=d_filter.days)
        query = query.where(Order.created_at >= ago)
    elif d_type == "before" and d_filter.before_date:
        query = query.where(Order.created_at < d_filter.before_date)
    elif d_type == "after" and d_filter.after_date:
        query = query.where(Order.created_at > d_filter.after_date)

    a_filter = req.amount_filter
    a_type = a_filter.filter_type
    if a_type == "between":
        query = query.having(func.sum(Order.amount).between(
            a_filter.min_value, a_filter.max_value))
    elif a_type == "gte":
        query = query.having(func.sum(Order.amount) >= a_filter.amount)
    elif a_type == "lte":
        query = query.having(func.sum(Order.amount) <= a_filter.amount)

    result = await db.execute(query)
    raw_rows = result.all()

    rows = []
    for account_id, name, total_amount in raw_rows:
        row = {
            "account_id": account_id,
            "name": name,
            "amount": int(total_amount)
        }
        rows.append(row)

    return rows

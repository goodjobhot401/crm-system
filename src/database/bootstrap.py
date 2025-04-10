import asyncio
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncEngine
from infra.session import engine
from infra.session import AsyncSessionLocal
from models.base import Base
from models.account import Account
from models.order import Order
from models.message import Message
from models.message_log import MessageLog


async def wait_for_connection(engine: AsyncEngine, retries: int = 10, delay: int = 2):
    for i in range(retries):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                print("MySQL is ready!")
                return
        except OperationalError as e:
            print(f"MySQL connection retry: {i+1}/{retries} - {str(e)}")
            await asyncio.sleep(delay)
    raise Exception(f"MySQL connection failed")


# async def create_seed_data():
#     async with AsyncSessionLocal() as session:
#         account_service = AccountService(db=session)
#         coupon_service = CouponService(db=session)
#         record_service = CouponRecordService(db=session, redis=redis_client)

#         await account_service.create_seeds()
#         await coupon_service.create_seeds()
#         await record_service.create_seeds()
#         print("Seed data created")


async def bootstrap():
    await wait_for_connection(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # await create_seed_data()


if __name__ == "__main__":
    asyncio.run(bootstrap())

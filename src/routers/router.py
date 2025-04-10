from fastapi import APIRouter
from routers.endpoints.account import router as account_router
from routers.endpoints.order import router as order_router
from routers.endpoints.message import router as message_router

router = APIRouter()

router.include_router(account_router, prefix="/account", tags=["Account"])
router.include_router(order_router, prefix="/order", tags=["Order"])
router.include_router(message_router, prefix="/message", tags=["Message"])

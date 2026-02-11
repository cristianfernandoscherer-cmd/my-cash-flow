from fastapi import APIRouter
from . import webhooks, transactions, health

router = APIRouter()

router.include_router(webhooks.router)
router.include_router(transactions.router)
router.include_router(health.router)
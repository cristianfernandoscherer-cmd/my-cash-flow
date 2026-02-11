from fastapi import APIRouter, Depends
import asyncpg
from datetime import datetime

from ...infra.data.database import get_db
from ..viewmodels.schemas import HealthResponse
from ...infra.core.config import settings
from ...infra.core.logger import logger

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
async def health_check(db: asyncpg.Pool = Depends(get_db)):
    """Health check do serviço"""
    try:
        await db.fetchval("SELECT 1")
        db_status = "connected"
    except Exception as e:
        logger.error(f"❌ Erro na conexão com banco: {str(e)}")
        db_status = "disconnected"
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        timestamp=datetime.now(),
        database=db_status
    )
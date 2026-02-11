import asyncpg
from typing import AsyncGenerator
from ..core.config import settings
from ..core.logger import logger

class Database:
    def __init__(self):
        self.pool: asyncpg.Pool = None
    
    async def connect(self):
        """Conecta ao banco de dados"""
        try:
            self.pool = await asyncpg.create_pool(
                dsn=settings.DATABASE_URL,
                min_size=settings.DB_POOL_MIN,
                max_size=settings.DB_POOL_MAX,
                command_timeout=60
            )
            logger.info("✅ Conectado ao PostgreSQL")
            
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao banco: {str(e)}")
            raise
    
    async def disconnect(self):
        """Desconecta do banco de dados"""
        if self.pool:
            await self.pool.close()
            logger.info("❌ Desconectado do PostgreSQL")

# Instância global do banco
db = Database()

async def get_db() -> asyncpg.Pool:
    """Dependency para obter conexão do pool"""
    return db.pool
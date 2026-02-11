import asyncpg
from typing import Optional, List, Dict, Any
from decimal import Decimal
from datetime import datetime
from ....domain.interfaces.repositories.itransaction_repository import ITransactionRepository
from ....domain.models.transaction import Transaction, TransactionCreate
from ....infra.core.logger import logger

class TransactionRepository(ITransactionRepository):
    def __init__(self, db_pool: asyncpg.Pool):
        self.db = db_pool
    
    async def create(self, transaction: TransactionCreate) -> Optional[Transaction]:
        """Cria uma nova transação (Gasto)"""
        try:
            row = await self.db.fetchrow("""
                INSERT INTO transactions (
                    item, valor, data, categoria, transaction_type, descricao
                ) VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING *
            """,
                transaction.item,
                transaction.valor,
                transaction.data,
                transaction.categoria,
                transaction.transaction_type,
                transaction.descricao
            )
            
            logger.info(f"✅ Transação registrada [{transaction.transaction_type}]: {transaction.item} - R$ {transaction.valor}")
            return Transaction(**dict(row)) if row else None
            
        except Exception as e:
            logger.error(f"Erro ao criar transação: {str(e)}")
            return None

    async def list_by_period(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Transaction]:
        """Lista transações por período"""
        try:
            rows = await self.db.fetch("""
                SELECT * FROM transactions
                WHERE data BETWEEN $1 AND $2
                ORDER BY data DESC, created_at DESC
            """, start_date, end_date)

            return [Transaction(**dict(row)) for row in rows]

        except Exception as e:
            logger.error(f"Erro ao listar transações por período: {str(e)}")
            return []

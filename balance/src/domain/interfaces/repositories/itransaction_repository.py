from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from ...models.transaction import Transaction, TransactionCreate
from datetime import datetime

class ITransactionRepository(ABC):
    @abstractmethod
    async def create(self, transaction: TransactionCreate) -> Optional[Transaction]:
        pass
    
    @abstractmethod
    async def list_by_period(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Transaction]:
        """
        Retorna uma lista de transações dentro de um período específico.
        """
        pass

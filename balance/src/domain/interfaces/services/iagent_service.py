from abc import ABC, abstractmethod
from typing import Optional
from ...models.transaction import TransactionCreate

class IAgentService(ABC):
    @abstractmethod
    async def parse_expense(self, text: str) -> Optional[TransactionCreate]:
        """Interpreta uma mensagem de texto e retorna uma transação estruturada"""
        pass

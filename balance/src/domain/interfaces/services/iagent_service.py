from abc import ABC, abstractmethod
from typing import Optional, List
from ...models.transaction import TransactionCreate

class IAgentService(ABC):
    @abstractmethod
    async def parse_expense(self, text: str) -> List[TransactionCreate]:
        """Interpreta uma mensagem de texto e retorna uma lista de transações estruturadas"""
        pass

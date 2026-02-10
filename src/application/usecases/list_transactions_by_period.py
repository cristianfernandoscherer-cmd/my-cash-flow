from datetime import datetime
from decimal import Decimal
from typing import List, Tuple
from ...domain.interfaces.repositories.itransaction_repository import ITransactionRepository
from ...domain.models.transaction import Transaction


class ListTransactionsByPeriod:
    def __init__(self, repo: ITransactionRepository):
        self.repo = repo

    async def execute(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> Tuple[List[Transaction], Decimal]:

        transactions = await self.repo.list_by_period(
            start_date=start_date,
            end_date=end_date,
        )

        total = Decimal("0.00")

        for t in transactions:
            if t.transaction_type == "income":
                total += t.valor
            else:
                total -= t.valor

        return transactions, total

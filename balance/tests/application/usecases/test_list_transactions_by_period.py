import pytest
from decimal import Decimal
from datetime import datetime
from unittest.mock import AsyncMock, Mock

from src.application.usecases.list_transactions_by_period import ListTransactionsByPeriod
from src.domain.models.transaction import Transaction

@pytest.mark.asyncio
async def test_list_transactions_by_period_execute():
    # Arrange
    mock_repo = AsyncMock()
    
    t1 = Mock(spec=Transaction)
    t1.valor = Decimal("100.00")
    t1.transaction_type = "income"
    
    t2 = Mock(spec=Transaction)
    t2.valor = Decimal("50.00")
    t2.transaction_type = "expense"
    
    mock_repo.list_by_period.return_value = [t1, t2]
    
    use_case = ListTransactionsByPeriod(mock_repo)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 31)
    
    # Act
    transactions, total = await use_case.execute(start_date, end_date)
    
    # Assert
    assert len(transactions) == 2
    assert total == Decimal("50.00") # 100 - 50
    mock_repo.list_by_period.assert_awaited_once_with(start_date=start_date, end_date=end_date)

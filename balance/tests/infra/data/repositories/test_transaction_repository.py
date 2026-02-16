import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime, date
from decimal import Decimal

from src.infra.data.repositories.transaction_repository import TransactionRepository
from src.domain.models.transaction import TransactionCreate, Transaction

@pytest.mark.asyncio
async def test_create_transaction_success():
    # Arrange
    mock_pool = AsyncMock()
    mock_row = {
        "id": 1,
        "item": "Test Item",
        "valor": Decimal("10.00"),
        "data": date(2023, 1, 1),
        "categoria": "Food",
        "transaction_type": "expense",
        "descricao": "Test Desc",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    mock_pool.fetchrow.return_value = mock_row
    
    repo = TransactionRepository(mock_pool)
    
    transaction_create = TransactionCreate(
        item="Test Item",
        valor=Decimal("10.00"),
        data=date(2023, 1, 1),
        categoria="Food",
        descricao="Test Desc",
        transaction_type="expense"
    )
    
    # Act
    result = await repo.create(transaction_create)
    
    # Assert
    assert result is not None
    assert isinstance(result, Transaction)
    assert result.item == "Test Item"
    assert result.id == 1
    mock_pool.fetchrow.assert_called_once()

@pytest.mark.asyncio
async def test_create_transaction_failure():
    # Arrange
    mock_pool = AsyncMock()
    mock_pool.fetchrow.side_effect = Exception("Database error")
    
    repo = TransactionRepository(mock_pool)
    
    transaction_create = TransactionCreate(
        item="Test Item",
        valor=Decimal("10.00"),
        data=date(2023, 1, 1),
        categoria="Food",
        descricao="Test Desc",
        transaction_type="expense"
    )
    
    # Act
    result = await repo.create(transaction_create)
    
    # Assert
    assert result is None
    mock_pool.fetchrow.assert_called_once()

@pytest.mark.asyncio
async def test_list_by_period_success():
    # Arrange
    mock_pool = AsyncMock()
    mock_row1 = {
        "id": 1,
        "item": "Test Item 1",
        "valor": Decimal("10.00"),
        "data": date(2023, 1, 1),
        "categoria": "Food",
        "transaction_type": "expense",
        "descricao": "Test Desc 1",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    mock_row2 = {
        "id": 2,
        "item": "Test Item 2",
        "valor": Decimal("20.00"),
        "data": date(2023, 1, 2),
        "categoria": "Work",
        "transaction_type": "income",
        "descricao": "Test Desc 2",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    mock_pool.fetch.return_value = [mock_row1, mock_row2]
    
    repo = TransactionRepository(mock_pool)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 31)
    
    # Act
    result = await repo.list_by_period(start_date, end_date)
    
    # Assert
    assert len(result) == 2
    assert isinstance(result[0], Transaction)
    assert result[0].id == 1
    assert result[1].id == 2
    mock_pool.fetch.assert_called_once()

@pytest.mark.asyncio
async def test_list_by_period_failure():
    # Arrange
    mock_pool = AsyncMock()
    mock_pool.fetch.side_effect = Exception("Database error")
    
    repo = TransactionRepository(mock_pool)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 31)
    
    # Act
    result = await repo.list_by_period(start_date, end_date)
    
    # Assert
    assert result == []
    mock_pool.fetch.assert_called_once()

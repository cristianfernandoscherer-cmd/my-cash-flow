import pytest
from unittest.mock import AsyncMock, Mock

from src.application.usecases.process_telegram_message import ProcessTelegramMessage
from src.domain.models.transaction import TransactionCreate

@pytest.mark.asyncio
async def test_process_telegram_message_success():
    # Arrange
    mock_repo = AsyncMock()
    mock_agent = AsyncMock()
    
    mock_transaction = Mock(spec=TransactionCreate)
    mock_transaction.item = "Coffee"
    mock_transaction.data = "2024-01-15"
    
    mock_agent.parse_expense.return_value = [mock_transaction]
    mock_repo.create.return_value = True
    
    use_case = ProcessTelegramMessage(mock_repo, mock_agent)
    
    # Act
    result = await use_case.execute("Buy coffee 10")
    
    # Assert
    assert result is True
    mock_agent.parse_expense.assert_awaited_once_with("Buy coffee 10")
    mock_repo.create.assert_awaited_once_with(mock_transaction)

@pytest.mark.asyncio
async def test_process_telegram_message_parse_fail():
    # Arrange
    mock_repo = AsyncMock()
    mock_agent = AsyncMock()
    
    mock_agent.parse_expense.return_value = []
    
    use_case = ProcessTelegramMessage(mock_repo, mock_agent)
    
    # Act
    result = await use_case.execute("Invalid message")
    
    # Assert
    assert result is False
    mock_agent.parse_expense.assert_awaited_once_with("Invalid message")
    mock_repo.create.assert_not_called()

@pytest.mark.asyncio
async def test_process_telegram_message_save_fail():
    # Arrange
    mock_repo = AsyncMock()
    mock_agent = AsyncMock()
    
    mock_transaction = Mock(spec=TransactionCreate)
    mock_transaction.item = "Coffee"
    mock_transaction.data = "2024-01-15"
    
    mock_agent.parse_expense.return_value = [mock_transaction]
    mock_repo.create.return_value = False
    
    use_case = ProcessTelegramMessage(mock_repo, mock_agent)
    
    # Act
    result = await use_case.execute("Buy coffee 10")
    
    # Assert
    assert result is False
    mock_repo.create.assert_awaited_once_with(mock_transaction)

@pytest.mark.asyncio
async def test_process_telegram_message_multiple_transactions():
    """Test processing message that generates multiple transactions (installments)"""
    # Arrange
    mock_repo = AsyncMock()
    mock_agent = AsyncMock()
    
    mock_tx1 = Mock(spec=TransactionCreate)
    mock_tx1.item = "Tenis"
    mock_tx1.data = "2024-01-20"
    
    mock_tx2 = Mock(spec=TransactionCreate)
    mock_tx2.item = "Tenis"
    mock_tx2.data = "2024-02-20"
    
    mock_agent.parse_expense.return_value = [mock_tx1, mock_tx2]
    mock_repo.create.return_value = True
    
    use_case = ProcessTelegramMessage(mock_repo, mock_agent)
    
    # Act
    result = await use_case.execute("Tenis parcelado 2x")
    
    # Assert
    assert result is True
    mock_agent.parse_expense.assert_awaited_once_with("Tenis parcelado 2x")
    assert mock_repo.create.await_count == 2
    mock_repo.create.assert_any_await(mock_tx1)
    mock_repo.create.assert_any_await(mock_tx2)

@pytest.mark.asyncio
async def test_process_telegram_message_partial_save():
    """Test when some transactions save successfully and others fail"""
    # Arrange
    mock_repo = AsyncMock()
    mock_agent = AsyncMock()
    
    mock_tx1 = Mock(spec=TransactionCreate)
    mock_tx1.item = "Tenis"
    mock_tx1.data = "2024-01-20"
    
    mock_tx2 = Mock(spec=TransactionCreate)
    mock_tx2.item = "Tenis"
    mock_tx2.data = "2024-02-20"
    
    mock_agent.parse_expense.return_value = [mock_tx1, mock_tx2]
    # First save succeeds, second fails
    mock_repo.create.side_effect = [True, False]
    
    use_case = ProcessTelegramMessage(mock_repo, mock_agent)
    
    # Act
    result = await use_case.execute("Tenis parcelado 2x")
    
    # Assert
    # Should return True if at least one saved successfully
    assert result is True
    assert mock_repo.create.await_count == 2


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
    
    mock_agent.parse_expense.return_value = mock_transaction
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
    
    mock_agent.parse_expense.return_value = None
    
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
    
    mock_agent.parse_expense.return_value = mock_transaction
    mock_repo.create.return_value = False
    
    use_case = ProcessTelegramMessage(mock_repo, mock_agent)
    
    # Act
    result = await use_case.execute("Buy coffee 10")
    
    # Assert
    assert result is False
    mock_repo.create.assert_awaited_once_with(mock_transaction)

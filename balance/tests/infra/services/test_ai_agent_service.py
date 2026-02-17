import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import date
from decimal import Decimal

from src.infra.services.ai_agent_service import AIAgentService
from src.domain.models.transaction import TransactionCreate


@pytest.fixture
def ai_service():
    """Fixture to create AIAgentService with mocked OpenAI client"""
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
        service = AIAgentService()
        return service


@pytest.mark.asyncio
async def test_single_transaction_no_credit(ai_service):
    """Test single transaction without credit card"""
    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='''{
        "item": "Cafe",
        "valor": 10.00,
        "data": "2024-01-15",
        "categoria": "Alimentacao",
        "transaction_type": "expense",
        "parcelas": 1,
        "metodo_pagamento": "debito",
        "descricao": "Cafe da manha"
    }'''))]
    
    ai_service.client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    # Act
    transactions = await ai_service.parse_expense("Cafe da manha")
    
    # Assert
    assert len(transactions) == 1
    assert transactions[0].item == "Cafe"
    assert transactions[0].valor == Decimal("10.00")
    assert transactions[0].data == date(2024, 1, 15)


@pytest.mark.asyncio
async def test_credit_card_after_26th_shifts_to_next_month(ai_service):
    """Test that credit card purchases after 26th are shifted to next month"""
    # Mock OpenAI response with date after 26th
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='''{
        "item": "Tenis",
        "valor": 100.00,
        "data": "2024-01-27",
        "categoria": "Vestuario",
        "transaction_type": "expense",
        "parcelas": 1,
        "metodo_pagamento": "credito",
        "descricao": "Tenis de corrida"
    }'''))]
    
    ai_service.client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    # Act
    transactions = await ai_service.parse_expense("Tenis de corrida no credito")
    
    # Assert
    assert len(transactions) == 1
    # Date should be shifted from 2024-01-27 to 2024-02-27
    assert transactions[0].data == date(2024, 2, 27)


@pytest.mark.asyncio
async def test_credit_card_on_or_before_26th_no_shift(ai_service):
    """Test that credit card purchases on or before 26th are not shifted"""
    # Mock OpenAI response with date on 26th
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='''{
        "item": "Livro",
        "valor": 50.00,
        "data": "2024-01-26",
        "categoria": "Educacao",
        "transaction_type": "expense",
        "parcelas": 1,
        "metodo_pagamento": "credito",
        "descricao": "Livro de programacao"
    }'''))]
    
    ai_service.client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    # Act
    transactions = await ai_service.parse_expense("Livro de programacao no credito")
    
    # Assert
    assert len(transactions) == 1
    # Date should NOT be shifted
    assert transactions[0].data == date(2024, 1, 26)


@pytest.mark.asyncio
async def test_installments_creates_multiple_transactions(ai_service):
    """Test that installment purchases create multiple transactions"""
    # Mock OpenAI response with 4 installments
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='''{
        "item": "Tenis Masculino",
        "valor": 100.00,
        "data": "2024-01-20",
        "categoria": "Vestuario",
        "transaction_type": "expense",
        "parcelas": 4,
        "metodo_pagamento": "credito",
        "descricao": "Tenis masculino parcelado"
    }'''))]
    
    ai_service.client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    # Act
    transactions = await ai_service.parse_expense("Tenis masculino parcelado em 4x")
    
    # Assert
    assert len(transactions) == 4
    
    # Check each installment
    expected_dates = [
        date(2024, 1, 20),
        date(2024, 2, 20),
        date(2024, 3, 20),
        date(2024, 4, 20)
    ]
    
    for i, tx in enumerate(transactions):
        assert tx.item == "Tenis Masculino"
        assert tx.valor == Decimal("25.00")  # 100 / 4
        assert tx.data == expected_dates[i]
        assert f"Parcela {i+1}/4" in tx.descricao
        assert tx.categoria == "Vestuario"


@pytest.mark.asyncio
async def test_installments_after_26th_shifts_all_dates(ai_service):
    """Test that installments after 26th shift all installment dates"""
    # Mock OpenAI response with installments after 26th
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='''{
        "item": "Notebook",
        "valor": 400.00,
        "data": "2024-01-27",
        "categoria": "Tecnologia",
        "transaction_type": "expense",
        "parcelas": 4,
        "metodo_pagamento": "credito",
        "descricao": "Notebook parcelado"
    }'''))]
    
    ai_service.client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    # Act
    transactions = await ai_service.parse_expense("Notebook parcelado em 4x no credito")
    
    # Assert
    assert len(transactions) == 4
    
    # All dates should be shifted by 1 month (from Jan 27 to Feb 27, then Mar 27, etc.)
    expected_dates = [
        date(2024, 2, 27),
        date(2024, 3, 27),
        date(2024, 4, 27),
        date(2024, 5, 27)
    ]
    
    for i, tx in enumerate(transactions):
        assert tx.data == expected_dates[i]
        assert tx.valor == Decimal("100.00")  # 400 / 4


@pytest.mark.asyncio
async def test_error_handling_returns_empty_list(ai_service):
    """Test that errors return empty list instead of None"""
    # Mock OpenAI to raise an exception
    ai_service.client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))
    
    # Act
    transactions = await ai_service.parse_expense("Some message")
    
    # Assert
    assert transactions == []


@pytest.mark.asyncio
async def test_debit_card_after_26th_no_shift(ai_service):
    """Test that debit card purchases after 26th are NOT shifted"""
    # Mock OpenAI response with debit after 26th
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='''{
        "item": "Supermercado",
        "valor": 200.00,
        "data": "2024-01-28",
        "categoria": "Alimentacao",
        "transaction_type": "expense",
        "parcelas": 1,
        "metodo_pagamento": "debito",
        "descricao": "Compras do mes"
    }'''))]
    
    ai_service.client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    # Act
    transactions = await ai_service.parse_expense("Compras do mes no debito")
    
    # Assert
    assert len(transactions) == 1
    # Date should NOT be shifted for debit
    assert transactions[0].data == date(2024, 1, 28)

import pytest
from unittest.mock import Mock, patch
from src.services import get_balance

@patch("src.services.requests.get")
@patch("src.services.os.getenv")
def test_get_balance_success(mock_getenv, mock_get):
    # Arrange
    mock_getenv.return_value = "http://mock-url"
    
    mock_response = Mock()
    mock_response.json.return_value = {"balance": "100.00", "total": 5}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    # Act
    result = get_balance.invoke({"start_date": "2023-01-01", "end_date": "2023-01-31"})
    
    # Assert
    assert "R$ 100.00" in result
    assert "Total de 5 transações" in result
    mock_get.assert_called_once()

@patch("src.services.requests.get")
@patch("src.services.os.getenv")
def test_get_balance_error(mock_getenv, mock_get):
    # Arrange
    mock_getenv.return_value = "http://mock-url"
    mock_get.side_effect = Exception("Connection error")
    
    # Act
    result = get_balance.invoke({"start_date": "2023-01-01", "end_date": "2023-01-31"})
    
    # Assert
    assert "Erro ao consultar saldo remoto" in result

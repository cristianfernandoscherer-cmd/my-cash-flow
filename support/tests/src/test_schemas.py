from src.schemas import ChatRequest
from pydantic import ValidationError
import pytest

def test_chat_request_valid():
    request = ChatRequest(
        message="Hello",
        session_id="123",
        client_id="456"
    )
    assert request.message == "Hello"
    assert request.session_id == "123"
    assert request.client_id == "456"

def test_chat_request_invalid_missing_field():
    with pytest.raises(ValidationError):
        ChatRequest(
            message="Hello",
            session_id="123"
            # client_id missing
        )

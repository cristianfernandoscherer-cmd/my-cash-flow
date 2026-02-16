from decimal import Decimal
from datetime import date
import pytest
from pydantic import ValidationError
from src.domain.models.transaction import TransactionBase

def test_transaction_base_valid():
    t = TransactionBase(
        item="Test Item",
        valor=Decimal("10.50"),
        data=date(2023, 1, 1),
        categoria="Food",
        descricao="Delicious food"
    )
    assert t.item == "Test Item"
    assert t.valor == Decimal("10.50")
    assert t.transaction_type == "expense"

def test_transaction_base_invalid_valor():
    with pytest.raises(ValidationError):
        TransactionBase(
            item="Test Item",
            valor=Decimal("0"), # Must be > 0
            data=date(2023, 1, 1),
            categoria="Food",
            descricao="Delicious food"
        )

def test_transaction_base_default_type():
    t = TransactionBase(
        item="Test Item",
        valor=Decimal("10.00"),
        data=date(2023, 1, 1),
        categoria="Salary",
        descricao="Work",
        transaction_type="income"
    )
    assert t.transaction_type == "income"

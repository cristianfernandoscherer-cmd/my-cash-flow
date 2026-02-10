from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal

class TransactionBase(BaseModel):
    item: str
    valor: Decimal = Field(gt=0)
    data: date
    categoria: str
    transaction_type: str = "expense"
    descricao: str  # Mensagem original

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

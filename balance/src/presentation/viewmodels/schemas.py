from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional

class ExpenseResponse(BaseModel):
    id: int
    item: str
    valor: Decimal
    data: date
    categoria: str
    descricao: str
    transaction_type: str
    created_at: datetime

class ExpenseListResponse(BaseModel):
    total: int
    balance: Decimal
    transactions: List[ExpenseResponse]

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: datetime
    database: str
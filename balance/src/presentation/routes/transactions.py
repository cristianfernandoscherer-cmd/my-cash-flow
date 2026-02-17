from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from ...infra.core.dependencies import get_transaction_repo
from ...domain.interfaces.repositories.itransaction_repository import ITransactionRepository
from ..viewmodels.schemas import ExpenseListResponse, ExpenseResponse
from ...infra.core.logger import logger
from datetime import date
from ...application.usecases.list_transactions_by_period import ListTransactionsByPeriod

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/period", response_model=ExpenseListResponse)
async def list_by_period(
    start_date: date = Query(..., description="Data inicial YYYY-MM-DD"),
    end_date: date = Query(..., description="Data final YYYY-MM-DD"),
    transaction_repo: ITransactionRepository = Depends(get_transaction_repo),
):
    """Lista transações por período e retorna o montante"""

    use_case = ListTransactionsByPeriod(transaction_repo)

    transactions, total = await use_case.execute(
        start_date=start_date,
        end_date=end_date,
    )

    return ExpenseListResponse(
        total=len(transactions),
        balance=total,
        transactions=[
            ExpenseResponse(
                id=t.id,
                item=t.item,
                valor=t.valor,
                data=t.data,
                categoria=t.categoria,
                descricao=t.descricao,
                transaction_type=t.transaction_type,
                created_at=t.created_at
            ) for t in transactions
        ]
    )

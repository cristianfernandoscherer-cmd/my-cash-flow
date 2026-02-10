import asyncpg
from fastapi import Depends
from ..data.database import get_db
from ..data.repositories.transaction_repository import TransactionRepository
from ...application.usecases.process_telegram_message import ProcessTelegramMessage

from ...domain.interfaces.repositories.itransaction_repository import ITransactionRepository
from ..services.ai_agent_service import AIAgentService
from ...domain.interfaces.services.iagent_service import IAgentService

def get_transaction_repo(db: asyncpg.Pool = Depends(get_db)) -> ITransactionRepository:
    """Dependency para TransactionRepository"""
    return TransactionRepository(db)

def get_ai_agent() -> IAgentService:
    """Dependency para o Agente de IA"""
    return AIAgentService()

def get_process_telegram_message(
    transaction_repo: ITransactionRepository = Depends(get_transaction_repo),
    agent: IAgentService = Depends(get_ai_agent)
) -> ProcessTelegramMessage:
    """Dependency para o caso de uso de processamento de mensagem"""
    return ProcessTelegramMessage(transaction_repo, agent)
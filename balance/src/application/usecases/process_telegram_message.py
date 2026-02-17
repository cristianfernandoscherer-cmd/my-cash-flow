from ...domain.interfaces.repositories.itransaction_repository import ITransactionRepository
from ...domain.interfaces.services.iagent_service import IAgentService
from ...infra.core.logger import logger
from typing import List

class ProcessTelegramMessage:
    def __init__(
        self, 
        transaction_repo: ITransactionRepository,
        agent: IAgentService
    ):
        self.transaction_repo = transaction_repo
        self.agent = agent

    async def execute(self, text: str) -> bool:
        """Orquestra o processamento da mensagem: interpretar -> salvar"""
        logger.info(f"🧠 Iniciando orquestração para: {text}")
        
        # 1. Interpretar com IA
        transactions = await self.agent.parse_expense(text)
        
        if not transactions:
            logger.warning(f"⚠️ IA não conseguiu interpretar mensagem ou nenhuma transação gerada: {text}")
            return False

        # 2. Salvar no Banco
        success_count = 0
        for transaction in transactions:
            saved = await self.transaction_repo.create(transaction)
            if saved:
                success_count += 1
                logger.info(f"✅ Gasto registrado com sucesso: {transaction.item} ({transaction.data})")
            else:
                logger.error(f"❌ Falha ao salvar gasto no banco: {transaction.item}")
        
        if success_count == len(transactions):
            return True
        elif success_count > 0:
            logger.warning(f"⚠️ Salvo parcialmente: {success_count}/{len(transactions)} transações")
            return True # Considera sucesso se salvou pelo menos um, mas loga warning
        else:
            return False

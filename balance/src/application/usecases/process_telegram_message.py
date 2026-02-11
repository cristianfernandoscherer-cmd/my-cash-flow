from ...domain.interfaces.repositories.itransaction_repository import ITransactionRepository
from ...domain.interfaces.services.iagent_service import IAgentService
from ...infra.core.logger import logger

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
        transaction_create = await self.agent.parse_expense(text)
        
        if not transaction_create:
            logger.warning(f"⚠️ IA não conseguiu interpretar mensagem: {text}")
            return False

        # 2. Salvar no Banco
        saved = await self.transaction_repo.create(transaction_create)
        
        if saved:
            logger.info(f"✅ Gasto registrado com sucesso: {transaction_create.item}")
            return True
        else:
            logger.error(f"❌ Falha ao salvar gasto no banco: {transaction_create.item}")
            return False

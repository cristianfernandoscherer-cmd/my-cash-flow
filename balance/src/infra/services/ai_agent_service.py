from openai import AsyncOpenAI
import json
import os
from typing import Optional
from datetime import date
from decimal import Decimal
from ...domain.interfaces.services.iagent_service import IAgentService
from ...domain.models.transaction import TransactionCreate
from ...infra.core.logger import logger

class AIAgentService(IAgentService):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY não encontrada no ambiente")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"

    async def parse_expense(self, text: str) -> Optional[TransactionCreate]:
        """Usa IA para extrair dados estruturados da mensagem"""
        today = date.today().isoformat()
        
        system_prompt = """
        Você é um assistente de finanças pessoais. Sua tarefa é extrair informações de uma mensagem de transação financeira.
        Extraia os seguintes campos em formato JSON:
        - item: O nome do produto, serviço ou origem do dinheiro (ex: "Tênis de corrida", "Salário", "Reembolso")
        - valor: O valor numérico (ex: 350.00)
        - data: A data no formato YYYY-MM-DD (se não houver uma data na mensagem, use a data de hoje)
        - categoria: Uma categoria curta (ex: "Vestimento", "Lazer", "Alimentação", "Salário", "Investimentos")
        - transaction_type: "expense" para gastos/despesas, ou "income" para ganhos/entradas de dinheiro.
        - descricao: A mensagem original na íntegra
        """

        user_prompt = f"""
        Mensagem: "{text}"
        Data de hoje: {today}
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            return TransactionCreate(
                item=data["item"],
                valor=Decimal(str(data["valor"])),
                data=data["data"],
                categoria=data["categoria"],
                transaction_type=data["transaction_type"],
                descricao=text
            )
        except Exception as e:
            logger.error(f"Erro ao interpretar mensagem com IA: {str(e)}")
            return None

from openai import AsyncOpenAI
import json
import os
from typing import Optional, List
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

    async def parse_expense(self, text: str) -> List[TransactionCreate]:
        """Usa IA para extrair dados estruturados da mensagem"""
        today = date.today().isoformat()
        
        system_prompt = """
        Você é um assistente de finanças pessoais. Sua tarefa é extrair informações de uma mensagem de transação financeira.
        Extraia os seguintes campos em formato JSON:
        - item: O nome do produto, serviço ou origem do dinheiro (ex: "Tênis de corrida", "Salário", "Reembolso")
        - valor: O valor total numérico (ex: 350.00)
        - data: A data no formato YYYY-MM-DD (se não houver uma data na mensagem, use a data de hoje)
        - categoria: Uma categoria curta (ex: "Vestimento", "Lazer", "Alimentação", "Salário", "Investimentos")
        - transaction_type: "expense" para gastos/despesas, ou "income" para ganhos/entradas de dinheiro.
        - parcelas: Número de parcelas (inteiro, padrão 1 se não mencionado)
        - metodo_pagamento: "credito" se for mencionado crédito ou parcelado, caso contrário "debito" ou outros.
        - descricao: A mensagem original na íntegra.
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
            
            transactions = []
            base_valor = Decimal(str(data["valor"]))
            base_date = date.fromisoformat(data["data"])
            parcelas = int(data.get("parcelas", 1))
            is_credit = data.get("metodo_pagamento") == "credito" or parcelas > 1
            
            if is_credit and base_date.day > 26:

                year = base_date.year + (base_date.month // 12)
                month = (base_date.month % 12) + 1

                try:
                    base_date = base_date.replace(year=year, month=month)
                except ValueError:
                    import calendar
                    last_day = calendar.monthrange(year, month)[1]
                    base_date = base_date.replace(year=year, month=month, day=last_day)
            
            installment_value = base_valor / parcelas
            
            for i in range(parcelas):
                year = base_date.year + ((base_date.month + i - 1) // 12)
                month = ((base_date.month + i - 1) % 12) + 1
                
                try:
                    current_date = base_date.replace(year=year, month=month)
                except ValueError:
                    import calendar
                    last_day = calendar.monthrange(year, month)[1]
                    current_date = base_date.replace(year=year, month=month, day=last_day)
                
                description = text
                if parcelas > 1:
                    description = f"{text} (Parcela {i+1}/{parcelas})"
                
                transactions.append(TransactionCreate(
                    item=data["item"],
                    valor=installment_value,
                    data=current_date,
                    categoria=data["categoria"],
                    transaction_type=data["transaction_type"],
                    descricao=description
                ))
            
            return transactions

        except Exception as e:
            logger.error(f"Erro ao interpretar mensagem com IA: {str(e)}")
            return []

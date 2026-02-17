from langchain_core.tools import tool
import requests
import logging
import os 
from typing import Optional

logger = logging.getLogger(__name__)

@tool
def get_balance(start_date: str, end_date: str, message: Optional[str] = None) -> str:
    """
    CONSULTA DE SALDO BANCÁRIO POR PERÍODO
    
    Esta ferramenta consulta o saldo bancário do cliente para um período específico.
    
    ARGS OBRIGATÓRIOS:
    - start_date: Data inicial NO FORMATO YYYY-MM-DD (ex: 2026-01-01)
    - end_date: Data final NO FORMATO YYYY-MM-DD (ex: 2026-12-31)
    
    ARGS OPCIONAL:
    - message: Mensagem adicional do cliente
    
    RETORNO:
    String com o saldo do período.
    """
    # Monta os query parameters
    params = {
        "start_date": start_date,
        "end_date": end_date
    }
    
    base_url = os.getenv('TRANSACTIONS_URL')

    url = f"{base_url}/api/v1/transactions/period"
    
    try:
        logger.info(f"➡️ Enviando requisição GET SALDO para {url}")
        logger.info(f"   Query params: {params}")
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(f"✅ Resposta SALDO recebida: {data}")
        
        # 🔥 ÚNICA MUDANÇA: Extrai o saldo e retorna uma string simples
        saldo = data.get("balance", "0.00")
        total = data.get("total", 0)
        
        return f"Seu saldo no período de {start_date} a {end_date} é R$ {saldo}. Total de {total} transações."
        
    except Exception as e:
        logger.exception("❌ Erro ao consultar saldo remoto")
        return f"Erro ao consultar saldo remoto: {str(e)}"

@tool
def get_income(start_date: str, end_date: str) -> dict:
    """
    CONSULTA DE RECEITAS (ENTRADAS) POR PERÍODO
    
    Esta ferramenta consulta os detalhes de dinheiro que ENTROU (receitas/income) em um período específico.
    Retorna uma lista de transações para o agente analisar.
    
    ARGS OBRIGATÓRIOS:
    - start_date: Data inicial NO FORMATO YYYY-MM-DD (ex: 2026-01-01)
    - end_date: Data final NO FORMATO YYYY-MM-DD (ex: 2026-01-31)
    
    RETORNO:
    Dicionário contendo a lista de transações e o total.
    """
    params = {
        "start_date": start_date,
        "end_date": end_date
    }
    
    base_url = os.getenv('TRANSACTIONS_URL')
    url = f"{base_url}/api/v1/transactions/period"
    
    try:
        logger.info(f"➡️ Buscando transações de RECEITA para {start_date} a {end_date}")
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Filtrar apenas transações de income
        all_transactions = data.get("transactions", [])
        income_transactions = [t for t in all_transactions if t.get("transaction_type") == "income"]
        
        total_income = sum(float(t.get("valor", 0)) for t in income_transactions)
        
        return {
            "period": {"start": start_date, "end": end_date},
            "total_value": total_income,
            "count": len(income_transactions),
            "transactions": income_transactions
        }
        
    except Exception as e:
        logger.exception("❌ Erro ao buscar receitas")
        return {"error": str(e)}

@tool
def get_expenses(start_date: str, end_date: str) -> dict:
    """
    CONSULTA DE DESPESAS (GASTOS) POR PERÍODO
    
    Esta ferramenta consulta os detalhes de dinheiro que SAIU (despesas/expenses) em um período específico.
    Retorna uma lista de transações para o agente analisar.
    
    ARGS OBRIGATÓRIOS:
    - start_date: Data inicial NO FORMATO YYYY-MM-DD (ex: 2026-01-01)
    - end_date: Data final NO FORMATO YYYY-MM-DD (ex: 2026-01-31)
    
    RETORNO:
    Dicionário contendo a lista de transações e o total.
    """
    params = {
        "start_date": start_date,
        "end_date": end_date
    }
    
    base_url = os.getenv('TRANSACTIONS_URL')
    url = f"{base_url}/api/v1/transactions/period"
    
    try:
        logger.info(f"➡️ Buscando transações de DESPESA para {start_date} a {end_date}")
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Filtrar apenas transações de expense
        all_transactions = data.get("transactions", [])
        expense_transactions = [t for t in all_transactions if t.get("transaction_type") == "expense"]
        
        total_expenses = sum(float(t.get("valor", 0)) for t in expense_transactions)
        
        return {
            "period": {"start": start_date, "end": end_date},
            "total_value": total_expenses,
            "count": len(expense_transactions),
            "transactions": expense_transactions
        }
        
    except Exception as e:
        logger.exception("❌ Erro ao buscar despesas")
        return {"error": str(e)}
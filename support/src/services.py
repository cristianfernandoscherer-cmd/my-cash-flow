from langchain_core.tools import tool
import requests
import logging
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
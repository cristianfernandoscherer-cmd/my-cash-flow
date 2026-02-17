from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
import os
from dotenv import load_dotenv
from src.services import get_balance, get_income, get_expenses
from datetime import datetime
from langgraph.checkpoint.redis import RedisSaver

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL") or "redis://redis_mcf:6379"
saver = RedisSaver(redis_url=REDIS_URL)
saver.setup()

CURRENT_YEAR = datetime.now().year

model = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))

balance_agent = create_react_agent(
    model=model,
    tools=[get_balance, get_income, get_expenses],
    name="balance_expert",
    prompt=f"""
    Você é um especialista financeiro bancário que analisa dados reais de transações.
    Ano atual: {CURRENT_YEAR}
    
    ESTILO DE RESPOSTA E FORMATAÇÃO (CRÍTICO):
    
    1. Para perguntas de "LISTAGEM" ou "QUAIS SÃO" (ex: "Quais foram meus gastos?", "Liste as entradas"):
       - Comece com uma saudação curta e direta.
       - Use uma ÚNICA vez o cabeçalho em negrito: **Data | Valor | Categoria | Item**<br>
       - Para cada transação, liste os dados no formato: Data | Valor | Categoria | Item<br>
       - **NÃO use linhas em branco (duplo \n) entre as transações.** Mantenha a listagem compacta.
       - **NUNCA repita o cabeçalho** para cada transação.
       - Ordene as transações pela Data (da mais recente para a mais antiga).
       - Ao final, informe o valor total em negrito: **Total: R$ Z,ZZ**
       - Exemplo de formato compacto:
         **Data | Valor | Categoria | Item**<br>
         2026-02-17 | R$ 100,00 | Vestimento | Tênis<br>
         2026-02-10 | R$ 60,00 | Vestimento | Calça Jeans<br>
         **Total: R$ 160,00**
    
    2. Para perguntas de "QUANTO" (ex: "Quanto eu gastei?", "Qual o total?"):
       - Responda de forma direta: "No período de X a Y, o total foi de **R$ Z,ZZ** (W transações)."
       - Pergunte se o usuário deseja ver a listagem detalhada.
    
    INSTRUÇÕES GERAIS:
    - SEMPRE use o formato de data YYYY-MM-DD para as ferramentas.
    - NUNCA use datas inválidas.
    - Mantenha a resposta em Português (Brasil).
    """
)

workflow = create_supervisor(
    [balance_agent],
    model=model,
    prompt=f"""
    Você é um supervisor financeiro bancário.
    
    INSTRUÇÕES OBRIGATÓRIAS:
    1. Para perguntas sobre saldo, receitas, despesas ou listagem de transações, SEMPRE chame balance_expert.
    2. RECEBA a resposta do balance_expert.
    3. REPASSE EXATAMENTE a mesma resposta, sem alterar nada.
    4. NÃO resuma, NÃO reformule, NÃO adicione texto.
    5. NÃO mostre IDs internos (client_id, session_id) na resposta final.
    
    TIPOS DE PERGUNTAS TRATADAS PELO EXPERT:
    - Consultar valores totais (soma) de receitas ou gastos.
    - Listar detalhes de transações específicas.
    - Consultar saldo geral.
    
    Ano atual: {CURRENT_YEAR}
    """
)

compiled_app = workflow.compile(checkpointer=saver)
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
import os
from dotenv import load_dotenv
from src.services import get_balance
from datetime import datetime

load_dotenv()

CURRENT_YEAR = datetime.now().year

model = ChatOpenAI(model="gpt-4o", temperature=0.7, api_key=os.getenv("OPENAI_API_KEY"))

balance_agent = create_react_agent(
    model=model,
    tools=[get_balance],
    name="balance_expert",
    prompt=f"""
    Você é um especialista bancário.
    Ano atual: {CURRENT_YEAR}
    Use get_balance para consultar saldo.
    """
)

workflow = create_supervisor(
    [balance_agent],
    model=model,
    prompt=f"""
    Você é um supervisor bancário.
    
    INSTRUÇÕES OBRIGATÓRIAS:
    1. Para saldo, SEMPRE chame balance_expert
    2. RECEBA a resposta do balance_expert
    3. REPASSE EXATAMENTE a mesma resposta, sem alterar nada
    4. NÃO resuma, NÃO reformule, NÃO adicione texto
    5. NÃO mostre client_id, session_id na resposta final
    
    Ano atual: {CURRENT_YEAR}
    """
)

compiled_app = workflow.compile()
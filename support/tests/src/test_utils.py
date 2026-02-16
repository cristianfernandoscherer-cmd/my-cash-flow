from src.utils import extrair_resposta_final
from langchain_core.messages import AIMessage, HumanMessage

def test_extrair_resposta_final_basic():
    messages = [
        HumanMessage(content="Hello"),
        AIMessage(content="Hi there")
    ]
    result = {"messages": messages}
    assert extrair_resposta_final(result) == "Hi there"

def test_extrair_resposta_final_no_ai_message():
    messages = [HumanMessage(content="Hello")]
    result = {"messages": messages}
    assert extrair_resposta_final(result) == "Nenhuma resposta encontrada."

def test_extrair_resposta_final_ignore_transfer():
    messages = [
        AIMessage(content="Transferring back to user"),
        AIMessage(content="Real answer")
    ]
    result = {"messages": messages}
    assert extrair_resposta_final(result) == "Real answer"

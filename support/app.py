import logging
import json
import time 
import os   
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.schemas import ChatRequest
from src.agents import compiled_app
from src.utils import extrair_resposta_final

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 🟢 Define start_time no nível do módulo (fora de qualquer função)
START_TIME = time.time()

# 🟢 Log de inicialização (executa quando o módulo é carregado)
logger.info("="*50)
logger.info("🚀 SUPPORT SERVICE INICIALIZANDO")
logger.info(f"📡 compiled_app carregado: {compiled_app is not None}")
logger.info(f"📡 PORT: {os.getenv('PORT', '8000')}")
logger.info(f"📡 TRANSACTIONS_URL: {os.getenv('TRANSACTIONS_URL', 'não configurada')}")
logger.info(f"🔑 OPENAI_API_KEY: {'configurada' if os.getenv('OPENAI_API_KEY') else 'NÃO CONFIGURADA'}")
logger.info("="*50)

@app.get("/health")
async def health_check():
    """Health check simplificado - apenas verifica se o app está vivo"""
    try:
        uptime = int(time.time() - START_TIME)
        return {
            "status": "alive",
            "service": "support",
            "uptime_seconds": uptime,
            "compiled_app": "loaded" if compiled_app is not None else "not_loaded",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "error": str(e)})

@app.get("/health/simple")
async def health_simple():
    """Health check ultra simples - não faz nada além de responder"""
    return {"status": "alive"}

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    if not payload.message:
        return JSONResponse(status_code=400, content={"error": "Campo 'message' é obrigatório"})
    try:
        logger.info(f"Mensagem recebida no /chat: {payload.message}")
        
        # 🟢 Verifica se compiled_app existe
        if compiled_app is None:
            logger.error("compiled_app não foi carregado!")
            return JSONResponse(status_code=500, content={"error": "Agente não disponível"})
            
        result = compiled_app.invoke({
            "messages": [{"role": "user", "content": f"{payload.message} session_id: {payload.session_id} client_id: {payload.client_id}"}]
        })
        resposta = extrair_resposta_final(result)
        logger.info(f"Resposta gerada: {resposta}")
        return {"resposta": resposta}
    except Exception as e:
        logger.exception("Erro ao processar requisição no endpoint /chat")
        return JSONResponse(status_code=500, content={"error": str(e)})
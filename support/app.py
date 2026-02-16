import logging
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.schemas import ChatRequest
from src.agents import compiled_app
from src.utils import extrair_resposta_final
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    if not payload.message:
        return JSONResponse(status_code=400, content={"error": "Campo 'message' é obrigatório"})
    try:
        logger.info(f"Mensagem recebida no /chat: {payload.message}")
        result = compiled_app.invoke({
            "messages": [{"role": "user", "content": f"{payload.message} session_id: {payload.session_id} client_id: {payload.client_id}"}]
        })
        resposta = extrair_resposta_final(result)
        logger.info(f"Resposta gerada: {resposta}")
        return {"resposta": resposta}
    except Exception as e:
        logger.exception("Erro ao processar requisição no endpoint /chat")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/health")
async def health_check():
    """
    Endpoint de health check para o Railway
    Retorna o status da aplicação e dependências
    """
    try:
        # Verifica se o compiled_app está carregado
        app_status = "loaded" if compiled_app is not None else "not_loaded"
        
        # Calcula o uptime
        uptime_seconds = int(time.time() - start_time)
        
        # Testa rapidamente se o compiled_app responde (opcional)
        app_test = "ok"
        if compiled_app and hasattr(compiled_app, 'invoke'):
            try:
                # Teste simples para ver se o app responde
                test_result = compiled_app.invoke({
                    "messages": [{"role": "user", "content": "test"}]
                })
                app_test = "ok"
            except Exception as e:
                app_test = f"error: {str(e)[:50]}"
        
        return {
            "status": "healthy",
            "service": "support",
            "timestamp": time.time(),
            "uptime_seconds": uptime_seconds,
            "compiled_app": app_status,
            "app_test": app_test,
            "environment": {
                "port": os.getenv('PORT', '8000'),
                "transactions_url": os.getenv('TRANSACTIONS_URL', 'not_set'),
                "redis": "configured" if os.getenv('REDIS_URL') else "not_configured"
            }
        }
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )
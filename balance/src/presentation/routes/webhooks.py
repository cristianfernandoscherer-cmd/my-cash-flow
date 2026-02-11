from fastapi import APIRouter, Request, BackgroundTasks, Depends
from typing import Dict, Any
from ...application.usecases.process_telegram_message import ProcessTelegramMessage
from ...infra.core.dependencies import get_process_telegram_message
from ...infra.core.logger import logger

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/telegram")
async def handle_telegram_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    use_case: ProcessTelegramMessage = Depends(get_process_telegram_message)
):
    """Endpoint para receber mensagens do Bot do Telegram"""
    try:
        payload = await request.json()
        message = payload.get("message") or payload.get("edited_message")
        
        if not message or "text" not in message:
            return {"status": "ignored", "message": "No text message found"}

        text = message["text"]
        logger.info(f"📩 Nova mensagem do Telegram: {text}")

        background_tasks.add_task(use_case.execute, text)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"❌ Erro no webhook do Telegram: {str(e)}")
        return {"status": "error", "message": str(e)}
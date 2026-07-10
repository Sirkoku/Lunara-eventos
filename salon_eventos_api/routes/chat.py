from fastapi import APIRouter

from models.chat_models import MensajeRequest
from services.chat import procesar_chat

router = APIRouter()

@router.post("/chat")
def chat(data: MensajeRequest):
    return procesar_chat(data)
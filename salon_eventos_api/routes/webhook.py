from fastapi import APIRouter, Request
import os
from dotenv import load_dotenv
from services.chatbot import procesar_mensaje


load_dotenv()
router= APIRouter()


@router.get("/webhook")
async def verificar_webhook(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == os.getenv("META_VERIFY_TOKEN"):
        return int(challenge)

    return {"error": "Token inválido"}


@router.post("/webhook")
async def recibir_webhook(request: Request):

    data = await request.json()

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" in value:

            numero = value["messages"][0]["from"]
            mensaje = value["messages"][0]["text"]["body"]
            procesar_mensaje(numero, mensaje)                                                     
            
            print(f"📱 {numero}")
            print(f"💬 {mensaje}")

        elif "statuses" in value:

            print(f"📨 Estado: {value['statuses'][0]['status']}")

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}
# Logica de meta 

import os
import requests
from dotenv import load_dotenv

load_dotenv()


ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")

# print("TOKEN:", ACCESS_TOKEN)
print("PHONE_ID:", PHONE_NUMBER_ID)

URL = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"


def enviar_mensaje(numero: str, mensaje: str):

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    body = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": mensaje
        }
    }

    try:
        respuesta = requests.post(
            URL,
            headers=headers,
            json=body,
            timeout=10
        )

        print("Status:", respuesta.status_code)
        print("Respuesta:", respuesta.text)

        return respuesta.json()

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}
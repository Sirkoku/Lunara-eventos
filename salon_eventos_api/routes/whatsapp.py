from fastapi import APIRouter

from models.whatsapp_models import MensajeWhatsApp
from services.whatsapp import enviar_mensaje

router = APIRouter()


@router.post("/enviar")
def enviar(datos: MensajeWhatsApp):

    return enviar_mensaje(
        numero=datos.numero,
        mensaje=datos.mensaje
    )
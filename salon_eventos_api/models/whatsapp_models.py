from pydantic import BaseModel

class MensajeWhatsApp(BaseModel):
    numero: str
    mensaje: str
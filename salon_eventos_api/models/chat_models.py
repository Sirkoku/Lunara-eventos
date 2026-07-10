from pydantic import BaseModel

class MensajeRequest(BaseModel):
    mensaje: str

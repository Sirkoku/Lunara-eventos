from pydantic import BaseModel

    # Modelo de datos para la reserva
class ReservaRequest(BaseModel):
    fecha: str
    turno: str
    nombre_cliente: str
    telefono: str
    email: str = None  
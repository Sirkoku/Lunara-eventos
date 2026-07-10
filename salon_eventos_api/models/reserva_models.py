from pydantic import BaseModel

    # Modelo de datos para la reserva
class ReservaRequest(BaseModel):
    fecha: str
    turno: str
    nombre_cliente: str
    telefono: str
    email: str = None  
    
    
class ConfirmarSenaRequest(BaseModel):
        reserva_id: int
        
class EditarReservaRequest(BaseModel):
    id: int
    fecha: str | None = None
    turno: str | None = None
    estado: str | None = None
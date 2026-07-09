from repositories.cliente_repository import (
    get_cliente_by_telefono,
    crear_cliente
)

from repositories.reserva.repository import (
    obtener_reserva_por_fecha_y_turno,
    crear_reserva 
    )
from models.reserva_models import ReservaRequest

def reservar (data : ReservaRequest):
    reserva = obtener_reserva_por_fecha_y_turno(
    data.fecha,
    data.turno
)

if reserva and reserva[0] in [
    "pendiente_sena",
    "senado",
    "pagado"
]:
    return {
        "error": f"El turno {data.turno} del {data.fecha} ya está ocupado"
    }

from fastapi import APIRouter
from models.reserva_models import (
    ReservaRequest,
    ConfirmarSenaRequest,
    EditarReservaRequest
)
from services.reservas import (
    reservar,
    listar_reservas,
    confirmar_sena_reserva,
    confirmar_pago_reserva,
    eliminar_reserva,
    actualizar_reserva
)

router = APIRouter()


@router.post("/reservar")
def crear_reserva(data: ReservaRequest):
    return reservar(data)
@router.get("/reservas")
def obtener_reservas():
    return listar_reservas()
@router.post("/confirmar_sena")
def confirmar(data: ConfirmarSenaRequest):
    return confirmar_sena_reserva(data)
@router.post("/confirmar_pago")
def confirmar_pago(data: ConfirmarSenaRequest):
    return confirmar_pago_reserva(data)
@router.delete("/cancelar_reserva/{id}")
def cancelar_reserva(id: int):
    return eliminar_reserva(id)
@router.put("/editar_reserva")
def editar_reserva(data: EditarReservaRequest):
    return actualizar_reserva(data)
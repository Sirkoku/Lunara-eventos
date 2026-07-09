from fastapi import APIRouter
from models.reserva_models import ReservaRequest
from services.reservas import (
    reservar,
    listar_reservas
)
from models.reserva_models import ConfirmarSenaRequest
from services.reservas import confirmar_sena_reserva


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
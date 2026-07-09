from fastapi import APIRouter
from services.clientes import listar_clientes

router = APIRouter()


@router.get("/clientes")
def obtener_clientes():
    return listar_clientes()
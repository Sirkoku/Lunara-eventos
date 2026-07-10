from fastapi import APIRouter
from services.disponibilidad import obtener_disponibilidad

router = APIRouter()


@router.get("/disponibilidad")
def disponibilidad(fecha: str):
    
    print("Fecha",fecha)
    
    resultado = obtener_disponibilidad(fecha)
    
    
    
    return resultado
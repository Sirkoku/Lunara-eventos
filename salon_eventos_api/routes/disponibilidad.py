from fastapi import APIRouter
from services.disponibilidad import obtener_disponibilidad

router = APIRouter()


@router.get("/disponibilidad")
def disponibilidad(fecha: str):
    print("1. entro al endpoint")
    print("Fecha",fecha)
    
    resultado = obtener_disponibilidad(fecha)
    print("2.Salio del service")
    
    
    return resultado
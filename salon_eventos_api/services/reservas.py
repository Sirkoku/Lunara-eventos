from repositories.cliente_repository import (
    get_cliente_by_telefono,
    crear_cliente
)

from repositories.reserva_repository import (
    obtener_reserva_por_fecha_y_turno,
    crear_reserva 
    )

from repositories.reserva_repository import (
    obtener_reserva_por_fecha_y_turno,
    crear_reserva,
    obtener_toda_las_reservas
)

from models.reserva_models import (
    ReservaRequest,
    ConfirmarSenaRequest
)

from repositories.reserva_repository import confirmar_sena


def reservar(data: ReservaRequest):

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

    cliente = get_cliente_by_telefono(data.telefono)

    if not cliente:
        cliente = crear_cliente(
            data.nombre_cliente,
            data.telefono,
            data.email
        )

    crear_reserva(
        data.fecha,
        data.turno,
        cliente[0]
    )

    return {
        "mensaje": "Reserva creada con exito",
        "fecha": data.fecha,
        "turno": data.turno,
        "estado": "pendiente_sena",
        "cliente_id": cliente[0]
    }

def listar_reservas():
    resultado = obtener_toda_las_reservas()
    
    reservas = []
    
    for r in resultado:
        reservas.append({
            "id": r[0],
            "fecha": r[1],
            "turno": r[2],
            "estado": r[3],
            "nombre_cliente": r[4],
            "telefono_cliente": r[5],
            "email_cliente": r[6]
        })
    return {
        "total": len(reservas),
        "reservas": reservas
    }

def confirmar_sena_reserva(data: ConfirmarSenaRequest):
    confirmar_sena(data.reserva_id)
    
    return{
        "mensaje":"Seña confirmada"
    }
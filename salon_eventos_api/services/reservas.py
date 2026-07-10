from repositories.cliente_repository import (
    get_cliente_by_telefono,
    crear_cliente
)

from models.reserva_models import (
    ReservaRequest,
    ConfirmarSenaRequest,
    EditarReservaRequest
)

from repositories.reserva_repository import (
    obtener_reserva_por_fecha_y_turno,
    crear_reserva,
    obtener_todas_las_reservas,
    confirmar_sena,
    confirmar_pago,
    cancelar_reserva,
    obtener_reserva_por_id,
    editar_reserva
)


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
    resultado = obtener_todas_las_reservas()
    
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
    
def confirmar_pago_reserva(data: ConfirmarSenaRequest):
    confirmar_pago(data.reserva_id)
    
    return{
        "mensaje":"Pago confirmado"
    }

def eliminar_reserva(reserva_id):
    cancelar_reserva(reserva_id)
    
    return{
        "mensaje":"Reserva cancelada"
    }   

def actualizar_reserva(data: EditarReservaRequest):
    reserva = obtener_reserva_por_id(data.id)
    
    if not reserva:
        return {
            "error": "No existe una reserva con ese ID"
        }
    if not data.fecha and not data.turno and not data.estado:
        return {
            "error": "No se enviaron campos para actualizar"
        }
        
    editar_reserva(
        data.id,
        data.fecha,
        data.turno,
        data.estado
    )
    return {
        "mensaje": "Reserva actualizada con exito",
        "id": data.id
    }

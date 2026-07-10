from services.ia import interpretar_mensaje
from models.chat_models import MensajeRequest

from services.disponibilidad import obtener_disponibilidad
from services.reservas import reservar
from models.reserva_models import ReservaRequest

TURNOS_VALIDOS = [
    "manana",
    "mediodia",
    "tarde"
]


def procesar_chat(data: MensajeRequest):

    resultado = interpretar_mensaje(data.mensaje)

    if "error" in resultado:
        return resultado

    intencion = resultado.get("intencion")
    fecha = resultado.get("fecha")
    turno = resultado.get("turno")
    nombre = resultado.get("nombre")
    respuesta = resultado.get("respuesta")

    # Si pregunta disponibilidad y tiene fecha → consultar DB
    if intencion == "consultar_disponibilidad" and fecha:

        resultado_disponibilidad = obtener_disponibilidad(fecha)

        resultado["disponibilidad_real"] = resultado_disponibilidad["disponibilidad"]

    # Si quiere reservar y tiene todos los datos → crear reserva
    if intencion == "reservar" and fecha and turno and nombre:

        if turno in TURNOS_VALIDOS:

            reserva = reservar(
            ReservaRequest(
                fecha=fecha,
                turno=turno,
                nombre_cliente=nombre,
                telefono="pendiente",
                email=None
            )
        )

        resultado["reserva"] = reserva

    return resultado
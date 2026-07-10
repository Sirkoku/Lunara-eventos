from repositories.reserva_repository import obtener_reservas_por_fecha


def obtener_disponibilidad(fecha):
    

    resultados = obtener_reservas_por_fecha(fecha)
    
    turnos = ["manana", "mediodia", "tarde"]

    ocupados = [
        r[0]
        for r in resultados
        if r[1] in ["pendiente_sena", "senado", "pagado"]
    ]

    disponibilidad = {}

    for turno in turnos:
        disponibilidad[turno] = (
            "ocupado" if turno in ocupados else "libre"
        )

    return {
        "fecha": fecha,
        "disponibilidad": disponibilidad
    }
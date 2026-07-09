from db.database import get_connection

def obtener_reservas_por_fecha(fecha):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT turno, estado
        FROM reservas
        WHERE fecha = %s
    """, (fecha,))

    resultados = cur.fetchall()

    cur.close()
    conn.close()

    return resultados

def obtener_reservas_por_fecha_y_turno(fecha, turno):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT estado
        FROM reservas
        WHERE fecha = %s
        AND turno = %s
    """, (fecha, turno))

    resultado = cur.fetchone()

    cur.close()
    conn.close()

    return resultado


def crear_reserva(fecha, turno, cliente_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reservas (fecha, turno, estado, cliente_id)
        VALUES (%s, %s, %s, %s)
    """, (
        fecha,
        turno,
        "pendiente_sena",
        cliente_id
    ))

    conn.commit()

    cur.close()
    conn.close()
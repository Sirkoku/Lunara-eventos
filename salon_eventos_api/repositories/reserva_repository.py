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

def obtener_reserva_por_fecha_y_turno(fecha, turno):
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

def obtener_toda_las_reservas ():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT r.id, r.fecha, r.turno, r.estado,
                c.nombre, c.telefono, c.email
        FROM reservas r
        LEFT JOIN clientes c
        ON r.cliente_id = c.id
        ORDER BY r.fecha, r.turno
    """)

    resultados = cur.fetchall()

    cur.close()
    conn.close()

    return resultados
def confirmar_sena(reserva_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE reservas
        SET estado = 'senado'
        WHERE id = %s
    """, (reserva_id,))

    conn.commit()

    cur.close()
    conn.close()
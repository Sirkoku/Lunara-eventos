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

def obtener_todas_las_reservas ():
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
    
def confirmar_pago(reserva_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE reservas
        SET estado = 'pagado'
        WHERE id = %s
    """, (reserva_id,))

    conn.commit()

    cur.close()
    conn.close()
    
def cancelar_reserva(reserva_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM reservas
        WHERE id = %s
    """, (reserva_id,))

    conn.commit()

    cur.close()
    conn.close()
    
def obtener_reserva_por_id(reserva_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id
        FROM reservas
        WHERE id = %s
    """, (reserva_id,))

    resultado = cur.fetchone()

    cur.close()
    conn.close()

    return resultado

def editar_reserva(reserva_id, fecha=None, turno=None, estado=None):
    conn = get_connection()
    cur = conn.cursor()

    campos = []
    valores = []

    if fecha:
        campos.append("fecha = %s")
        valores.append(fecha)

    if turno:
        campos.append("turno = %s")
        valores.append(turno)

    if estado:
        campos.append("estado = %s")
        valores.append(estado)

    valores.append(reserva_id)

    cur.execute(f"""
        UPDATE reservas
        SET {', '.join(campos)}
        WHERE id = %s
    """, valores)

    conn.commit()

    cur.close()
    conn.close()
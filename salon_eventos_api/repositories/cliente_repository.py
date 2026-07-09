from db.database import get_connection

def get_cliente_by_telefono(telefono):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM clientes WHERE telefono = %s",
        (telefono,)
    )

    cliente = cur.fetchone()

    cur.close()
    conn.close()
    return cliente


def crear_cliente(nombre, telefono, email=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO clientes (nombre, telefono, email)
        VALUES (%s, %s)
        RETURNING *
        """,
        (nombre, telefono, email)
    )

    cliente = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return cliente
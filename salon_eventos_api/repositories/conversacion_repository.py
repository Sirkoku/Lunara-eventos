from db.database import get_connection


def guardar_mensaje(cliente_id, mensaje, rol):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO conversaciones (cliente_id, mensaje, rol)
        VALUES (%s, %s, %s)
        """,
        (cliente_id, mensaje, rol)
    )

    conn.commit()

    cur.close()
    conn.close()
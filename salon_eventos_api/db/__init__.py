from db.database import get_connection

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # CLIENTES
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id SERIAL PRIMARY KEY,
        nombre TEXT,
        telefono TEXT UNIQUE,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # EVENTOS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS eventos (
        id SERIAL PRIMARY KEY,
        cliente_id INTEGER REFERENCES clientes(id),
        fecha DATE,
        estado TEXT DEFAULT 'pendiente'
    );
    """)

    # RESERVAS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        id SERIAL PRIMARY KEY,
        cliente_id INTEGER REFERENCES clientes(id),
        evento_id INTEGER REFERENCES eventos(id),
        estado TEXT DEFAULT 'pendiente'
    );
    """)

    # PAGOS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pagos (
        id SERIAL PRIMARY KEY,
        reserva_id INTEGER REFERENCES reservas(id),
        monto NUMERIC,
        estado TEXT DEFAULT 'pendiente'
    );
    """)

    # CONVERSACIONES
    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversaciones (
        id SERIAL PRIMARY KEY,
        cliente_id INTEGER REFERENCES clientes(id),
        mensaje TEXT,
        rol TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Tablas creadas correctamente")


if __name__ == "__main__":
    create_tables()
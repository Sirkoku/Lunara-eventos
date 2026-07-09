from db.database import get_connection


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    # CLIENTES
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            telefono VARCHAR(20) UNIQUE NOT NULL,
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # EVENTOS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            id SERIAL PRIMARY KEY,
            cliente_id INTEGER REFERENCES clientes(id),
            fecha DATE,
            estado VARCHAR(30) DEFAULT 'pendiente'
        );
    """)

    # RESERVAS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id SERIAL PRIMARY KEY,
            cliente_id INTEGER REFERENCES clientes(id),
            evento_id INTEGER REFERENCES eventos(id),
            estado VARCHAR(30) DEFAULT 'pendiente'
        );
    """)

    # PAGOS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pagos (
            id SERIAL PRIMARY KEY,
            reserva_id INTEGER REFERENCES reservas(id),
            monto NUMERIC(10,2),
            estado VARCHAR(30) DEFAULT 'pendiente'
        );
    """)

    # CONVERSACIONES
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversaciones (
            id SERIAL PRIMARY KEY,
            cliente_id INTEGER REFERENCES clientes(id),
            mensaje TEXT NOT NULL,
            rol VARCHAR(20) NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Base de datos inicializada correctamente")


if __name__ == "__main__":
    create_tables()
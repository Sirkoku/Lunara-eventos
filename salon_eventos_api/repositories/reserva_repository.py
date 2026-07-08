from db.database import get_connection

def obtener_reservas_por_fecha(fecha):
    print("5. entro al repository")
    
    conn = get_connection()
    print("6. Conexion establecida")
    
    cur = conn.cursor()
    print("7. Cursor creado")

    cur.execute("""
                SELECT turno,estado
                FROM reservas
                Where fecha = %s
                """, (fecha,))
    resultados = cur.fetchall()
    
    print("8. consulta ok")  
    
    resultados = cur.fetchall()
    
    print("9, fetch ok",resultados)
    
    
    cur.close()
    conn.close()
    
    return resultados
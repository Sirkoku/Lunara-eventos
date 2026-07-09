from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router
import psycopg2
from pydantic import BaseModel
from routes.webhook import router as webhook_router
from routes.disponibilidad import router as disponibilidad_router
from models.reserva_models import ReservaRequest
app = FastAPI()

app.include_router(whatsapp_router)
app.include_router(webhook_router)
app.include_router(disponibilidad_router)

TURNOS_VALIDOS = ["manana","mediodia","tarde"]
ESTADOS_VALIDOS= ["pendiente_sena","senado","pagado"]

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Conexión a la base de datos
def get_conexion():
    return psycopg2.connect(
        host="localhost",
        database="salon_eventos",
        user="postgres",
        password="0401Giovanni"
    )
    
    print("conexion a postgre ok")

# Healthcheck — para verificar que el servidor está ok
@app.get("/health")
def health():
    return {"estado": "ok", "mensaje": "Servidor funcionando 🚀"}


@app.post("/reservar")
def reservar(data: ReservaRequest):
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        # Verificar si el turno ya está ocupado
        cursor.execute("""
            SELECT estado FROM public.reservas
            WHERE fecha = %s AND turno = %s
        """, (data.fecha, data.turno))

        resultado = cursor.fetchone()

        if resultado and resultado[0] in ["pendiente_sena", "senado", "pagado"]:
            cursor.close()
            conexion.close()
            return {"error": f"El turno {data.turno} del {data.fecha} ya está ocupado"}

        # Crear o buscar cliente
        cursor.execute("""
            SELECT id FROM public.clientes
            WHERE telefono = %s
        """, (data.telefono,))

        cliente = cursor.fetchone()

        if cliente:
            cliente_id = cliente[0]
        else:
            cursor.execute("""
                INSERT INTO public.clientes (nombre, telefono, email)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (data.nombre_cliente, data.telefono, data.email))
            cliente_id = cursor.fetchone()[0]

        # Insertar la reserva vinculada al cliente
        cursor.execute("""
            INSERT INTO public.reservas (fecha, turno, estado, cliente_id)
            VALUES (%s, %s, %s, %s)
        """, (data.fecha, data.turno, "pendiente_sena", cliente_id))

        conexion.commit()
        cursor.close()
        conexion.close()

        return {
            "mensaje": "Reserva creada con exito",
            "fecha": data.fecha,
            "turno": data.turno,
            "estado": "pendiente_sena",
            "cliente_id": cliente_id
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/reservas")
def listar_reservas():
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT r.id, r.fecha, r.turno, r.estado,
                c.nombre, c.telefono, c.email
            FROM public.reservas r
            LEFT JOIN public.clientes c ON r.cliente_id = c.id
            ORDER BY r.fecha, r.turno
        """)

        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()

        reservas = []
        for r in resultados:
            reservas.append({
                "id": r[0],
                "fecha": str(r[1]),
                "turno": r[2],
                "estado": r[3],
                "cliente": {
                    "nombre": r[4],
                    "telefono": r[5],
                    "email": r[6]
                }
            })

        return {"total": len(reservas), "reservas": reservas}

    except Exception as e:
        return {"error": str(e)}

class ConfirmarSenaRequest(BaseModel):
    id: int

@app.post("/confirmar_sena")
def confirmar_sena(data: ConfirmarSenaRequest):
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        # Verificar que la reserva existe y está en pendiente_sena
        cursor.execute("""
            SELECT id, estado FROM public.reservas
            WHERE id = %s
        """, (data.id,))

        resultado = cursor.fetchone()

        if not resultado:
            cursor.close()
            conexion.close()
            return {"error": "No existe una reserva con ese ID"}

        if resultado[1] != "pendiente_sena":
            cursor.close()
            conexion.close()
            return {"error": f"La reserva no está en estado pendiente_sena, está en: {resultado[1]}"}

        # Actualizar el estado a senado
        cursor.execute("""
            UPDATE public.reservas
            SET estado = 'senado'
            WHERE id = %s
        """, (data.id,))

        conexion.commit()
        cursor.close()
        conexion.close()

        return {
            "mensaje": "Seña confirmada con éxito ✅",
            "id": data.id,
            "estado": "senado"
        }

    except Exception as e:
        return {"error": str(e)}

@app.get("/clientes")
def listar_clientes():
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, telefono, email, created_at
            FROM public.clientes
            ORDER BY created_at DESC
        """)

        resultados = cursor.fetchall()
        cursor.close()
        conexion.close()

        clientes = []
        for c in resultados:
            clientes.append({
                "id": c[0],
                "nombre": c[1],
                "telefono": c[2],
                "email": c[3],
                "created_at": str(c[4])
            })

        return {"total": len(clientes), "clientes": clientes}

    except Exception as e:
        return {"error": str(e)}
    
class ConfirmarPagoRequest(BaseModel):
        id: int

@app.post("/confirmar_pago")
def confirmar_pago(data: ConfirmarPagoRequest):
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        # Verificar que la reserva existe y está en senado
        cursor.execute("""
            SELECT id, estado FROM public.reservas
            WHERE id = %s
        """, (data.id,))

        resultado = cursor.fetchone()

        if not resultado:
            cursor.close()
            conexion.close()
            return {"error": "No existe una reserva con ese ID"}

        if resultado[1] != "senado":
            cursor.close()
            conexion.close()
            return {"error": f"La reserva no está en estado senado, está en: {resultado[1]}"}

        # Actualizar el estado a pagado
        cursor.execute("""
            UPDATE public.reservas
            SET estado = 'pagado'
            WHERE id = %s
        """, (data.id,))

        conexion.commit()
        cursor.close()
        conexion.close()

        return {
            "mensaje": "Pago confirmado con exito",
            "id": data.id,
            "estado": "pagado"
        }

    except Exception as e:
        return {"error": str(e)}
    

class EditarReservaRequest(BaseModel):
    id: int
    fecha: str = None
    turno: str = None
    estado: str = None

@app.put("/editar_reserva")
def editar_reserva(data: EditarReservaRequest):
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        # Verificar que la reserva existe
        cursor.execute("""
            SELECT id FROM public.reservas
            WHERE id = %s
        """, (data.id,))

        if not cursor.fetchone():
            cursor.close()
            conexion.close()
            return {"error": "No existe una reserva con ese ID"}

        # Armar los campos a actualizar dinámicamente
        campos = []
        valores = []

        if data.fecha:
            campos.append("fecha = %s")
            valores.append(data.fecha)
        if data.turno:
            campos.append("turno = %s")
            valores.append(data.turno)
        if data.estado:
            campos.append("estado = %s")
            valores.append(data.estado)

        if not campos:
            cursor.close()
            conexion.close()
            return {"error": "No se enviaron campos para actualizar"}

        valores.append(data.id)

        cursor.execute(f"""
            UPDATE public.reservas
            SET {', '.join(campos)}
            WHERE id = %s
        """, valores)

        conexion.commit()
        cursor.close()
        conexion.close()

        return {
            "mensaje": "Reserva actualizada con exito",
            "id": data.id
        }

    except Exception as e:
        return {"error": str(e)}


@app.delete("/cancelar_reserva/{id}")
def cancelar_reserva(id: int):
    try:
        conexion = get_conexion()
        cursor = conexion.cursor()

        # Verificar que la reserva existe
        cursor.execute("""
            SELECT id FROM public.reservas
            WHERE id = %s
        """, (id,))

        if not cursor.fetchone():
            cursor.close()
            conexion.close()
            return {"error": "No existe una reserva con ese ID"}

        cursor.execute("""
            DELETE FROM public.reservas
            WHERE id = %s
        """, (id,))

        conexion.commit()
        cursor.close()
        conexion.close()

        return {"mensaje": f"Reserva {id} cancelada con exito"}

    except Exception as e:
        return {"error": str(e)}
    
    
    
from services.ia import interpretar_mensaje

class MensajeRequest(BaseModel):
    mensaje: str

@app.post("/chat")
def chat(data: MensajeRequest):
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
        try:
            conexion = get_conexion()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT turno, estado FROM public.reservas
                WHERE fecha = %s
            """, (fecha,))
            resultados = cursor.fetchall()
            cursor.close()
            conexion.close()

            ocupados = [r[0] for r in resultados if r[1] in ["pendiente_sena", "senado", "pagado"]]
            turnos = ["manana", "mediodia", "tarde"]
            disponibilidad = {t: "ocupado" if t in ocupados else "libre" for t in turnos}

            resultado["disponibilidad_real"] = disponibilidad

        except Exception as e:
            resultado["error_db"] = str(e)

    # Si quiere reservar y tiene todos los datos → crear reserva
    if intencion == "reservar" and fecha and turno and nombre:
        if turno in TURNOS_VALIDOS:
            try:
                conexion = get_conexion()
                cursor = conexion.cursor()

                cursor.execute("""
                    SELECT estado FROM public.reservas
                    WHERE fecha = %s AND turno = %s
                """, (fecha, turno))
                existente = cursor.fetchone()

                if existente and existente[0] in ["pendiente_sena", "senado", "pagado"]:
                    resultado["reserva"] = "turno_ocupado"
                    resultado["respuesta"] = f"Lo siento, el turno {turno} del {fecha} ya está ocupado. ¿Querés otro turno?"
                else:
                    cursor.execute("""
                        INSERT INTO public.clientes (nombre, telefono)
                        VALUES (%s, %s) RETURNING id
                    """, (nombre, "pendiente"))
                    cliente_id = cursor.fetchone()[0]

                    cursor.execute("""
                        INSERT INTO public.reservas (fecha, turno, estado, cliente_id)
                        VALUES (%s, %s, %s, %s) RETURNING id
                    """, (fecha, turno, "pendiente_sena", cliente_id))
                    reserva_id = cursor.fetchone()[0]

                    conexion.commit()
                    cursor.close()
                    conexion.close()

                    resultado["reserva"] = "creada"
                    resultado["reserva_id"] = reserva_id
                    resultado["respuesta"] = f"¡Perfecto {nombre}! Reserva creada para el {fecha} turno {turno}. Para confirmarla necesitamos la seña del 30%. ¿Nos mandás el comprobante?"

            except Exception as e:
                resultado["error_db"] = str(e)

    return resultado
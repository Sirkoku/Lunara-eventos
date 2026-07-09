from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router
import psycopg2
from pydantic import BaseModel
from routes.webhook import router as webhook_router
from routes.disponibilidad import router as disponibilidad_router
from models.reserva_models import ReservaRequest
from routes.reservas import router as reservas_router
from routes.clientes import router as clientes_router



app = FastAPI()

app.include_router(whatsapp_router)
app.include_router(webhook_router)
app.include_router(disponibilidad_router)
app.include_router(reservas_router)
app.include_router(clientes_router)



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
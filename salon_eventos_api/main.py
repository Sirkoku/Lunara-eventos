from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router
import psycopg2
from pydantic import BaseModel
from routes.webhook import router as webhook_router
from routes.disponibilidad import router as disponibilidad_router
from models.reserva_models import ReservaRequest
from routes.reservas import router as reservas_router
from routes.clientes import router as clientes_router
from services.ia import interpretar_mensaje


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



class EditarReservaRequest(BaseModel):
    id: int
    fecha: str = None
    turno: str = None
    estado: str = None



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
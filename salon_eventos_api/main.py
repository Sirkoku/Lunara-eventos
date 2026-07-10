from fastapi import FastAPI
from routes.whatsapp import router as whatsapp_router
from routes.webhook import router as webhook_router
from routes.disponibilidad import router as disponibilidad_router
from routes.reservas import router as reservas_router
from routes.clientes import router as clientes_router
from routes.chat import router as chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(whatsapp_router)
app.include_router(webhook_router)
app.include_router(disponibilidad_router)
app.include_router(reservas_router)
app.include_router(clientes_router)
app.include_router(chat_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Healthcheck — para verificar que el servidor está ok
@app.get("/health")
def health():
    return {"estado": "ok", "mensaje": "Servidor funcionando "}







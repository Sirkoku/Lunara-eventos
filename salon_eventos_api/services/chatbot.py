from repositories.cliente_repository import (
    get_cliente_by_telefono,
    crear_cliente
)

from repositories.conversacion_repository import (
    guardar_mensaje
)
from services.ia import interpretar_mensaje
from services.whatsapp import enviar_mensaje

def procesar_mensaje(numero, mensaje):

    cliente = get_cliente_by_telefono(numero)

    if not cliente:
        cliente = crear_cliente("Sin nombre", numero)
        print("✅ Cliente creado")
    else:
        print("👤 Cliente existente")

    guardar_mensaje(
        cliente["id"],
        mensaje,
        "usuario"
    )

    print("💾 Mensaje guardado")

    resultado = interpretar_mensaje(mensaje)
    respuesta = resultado["respuesta"]
    
    guardar_mensaje(
        cliente["id"],
        respuesta,
        "asistente"
        )
    print ("Enviando:",respuesta)
    
    enviar_mensaje(numero, respuesta)
    print(numero)
    print(mensaje)
    
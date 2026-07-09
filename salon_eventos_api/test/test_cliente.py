from repositories.cliente_repository import (
    get_cliente_by_telefono,
    crear_cliente
)

telefono = "5492230000000"

# 1. Buscar cliente
cliente = get_cliente_by_telefono(telefono)

if not cliente:
    print("No existe, creando cliente...")
    cliente = crear_cliente("Cliente Test",
    "54922XXXXXXXX",
    "test@test.com")
else:
    print("Cliente ya existe")

print(cliente)
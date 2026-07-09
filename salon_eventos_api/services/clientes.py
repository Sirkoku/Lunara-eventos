from repositories.cliente_repository import obtener_clientes


def listar_clientes():
    resultados = obtener_clientes()

    clientes = []

    for c in resultados:
        clientes.append({
            "id": c[0],
            "nombre": c[1],
            "telefono": c[2],
            "email": c[3]
        })

    return {
        "total": len(clientes),
        "clientes": clientes
    }
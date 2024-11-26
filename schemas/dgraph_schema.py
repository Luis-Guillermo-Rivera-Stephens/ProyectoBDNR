import pydgraph

def set_schema(client):
    client.alter(pydgraph.Operation(drop_all=True))
    schema = """
    type Juego {
        j_name
        description
        category
        related_with
    }

    type Categoria {
        c_name
    }

    # Juego Properties
    j_name: string @index(term) .
    description: string .
    category: uid .              # Relación con un Categoria (uid)
    related_with: [uid] .        # Lista de relaciones con otros Juegos (uid)

    # Categoria Properties
    c_name: string @index(term) .
    """
    op = pydgraph.Operation(schema=schema)
    client.alter(op)

import pydgraph

def set_schema(client):
    schema = """
    type Juego {
        _id
        name
        description
        category
        related_with
    }

    type Categoria {
        _id
        name
    }

    # Juego Properties
    _id: string @index(exact) . 
    name: string @index(term) . 
    description: string .       
    category: uid .             
    related_with: [uid] .        

    # Categoria Properties
    _id: string @index(exact) . 
    name: string @index(term) . 
    """
    op = pydgraph.Operation(schema=schema)
    client.alter(op)

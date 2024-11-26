from pydgraph import DgraphClient, DgraphClientStub
from models import dgraph_model  

# Conexión a Dgraph
stub = DgraphClientStub('localhost:9080')
client = DgraphClient(stub)

# Consulta: Obtener juegos de una categoría específica
def get_games_by_category(category_id):
    query = f"""
    {{
        games(func: eq(Categoria._id, "{category_id}")) {{
            _id
            name
            description
            related_with {{
                _id
                name
            }}
        }}
    }}
    """
    res = client.txn(read_only=True).query(query)
    return res.json

# Consulta: Buscar juegos por nombre (coincidencias parciales y exactas)
def get_games_by_name(name):
    query = f"""
    {{
        games(func: anyofterms(name, "{name}")) {{
            _id
            name
            description
            category {{
                _id
                name
            }}
        }}
    }}
    """
    res = client.txn(read_only=True).query(query)
    return res.json

# Consulta: Sugerir juegos basados en juegos jugados previamente
def get_suggested_games(user_played_game_ids):
    ids_str = ", ".join(f'"{id}"' for id in user_played_game_ids)
    query = f"""
    {{
        games(func: uid({ids_str})) {{
            related_with @filter(not uid({ids_str})) {{
                _id
                name
                description
            }}
        }}
    }}
    """
    res = client.txn(read_only=True).query(query)
    return res.json

# Consulta: Obtener juegos más populares (basado en un contador de juegos)
def get_most_popular_games(limit=10):
    query = f"""
    {{
        popular_games(func: has(name), orderdesc: played_counter, first: {limit}) {{
            _id
            name
            description
            played_counter
        }}
    }}
    """
    res = client.txn(read_only=True).query(query)
    return res.json

# Consulta: Juegos de la categoría favorita del usuario
def get_favorite_category_games(user_category_id):
    query = f"""
    {{
        favorite_games(func: eq(Categoria._id, "{user_category_id}")) {{
            _id
            name
            description
        }}
    }}
    """
    res = client.txn(read_only=True).query(query)
    return res.json

# Consulta: Obtener juegos relacionados con un juego específico
def get_related_games(game_id):
    query = f"""
    {{
        game(func: eq(Juego._id, "{game_id}")) {{
            related_with {{
                _id
                name
                description
            }}
        }}
    }}
    """
    res = client.txn(read_only=True).query(query)
    return res.json

# Consulta: Obtener categorías de juegos con la mayor actividad del usuario
def get_top_categories(user_id):
    query = f"""
    {{
        user(func: eq(User._id, "{user_id}")) {{
            categories_played @filter(gt(time_playing, 0)) (orderdesc: time_playing) {{
                category {{
                    name
                }}
                time_playing
            }}
        }}
    }}
    """
    res = client.txn(read_only=True).query(query)
    return res.json

# Cerrar conexión al terminar
def close_connection():
    stub.close()

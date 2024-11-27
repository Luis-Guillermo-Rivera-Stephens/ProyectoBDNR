from typing import Tuple, List
from models.mongo_schema import Game, Category
import uuid

def get_most_played_stats(session, account_id: uuid.UUID):
    """
    Obtiene los juegos más jugados y categorías más jugadas para un usuario
    
    Args:
        session: Sesión de MongoDB
        account_id: UUID del usuario
    
    Returns:
        Tuple con lista de juegos y lista de categorías más jugados para ese usuario
    """
    
    # Agregación para obtener los 3 juegos más jugados
    most_played_games_pipeline = [
        {
            "$match": {
                "userID": account_id
            }
        },
        {
            "$unwind": "$Games"
        },
        {
            "$project": {
                "game": "$Games"
            }
        },
        {
            "$sort": {
                "game.time_playing": -1
            }
        },
        {
            "$limit": 3
        },
        {
            "$project": {
                "_gameID": "$game.gameID",
                "played_counter": "$game.played_counter",
                "time_playing": "$game.time_playing",
                "category": "$game.category"
            }
        }
    ]

    # Agregación para obtener las 3 categorías más jugadas
    most_played_categories_pipeline = [
        {
            "$match": {
                "userID": account_id
            }
        },
        {
            "$unwind": "$Categories"
        },
        {
            "$project": {
                "category": "$Categories"
            }
        },
        {
            "$sort": {
                "category.time_playing": -1
            }
        },
        {
            "$limit": 2
        },
        {
            "$project": {
                "category": "$category.category",
                "time_playing": "$category.time_playing"
            }
        }
    ]

    # Ejecutar agregaciones
    games_result = list(session.database.users_info.aggregate(most_played_games_pipeline))
    categories_result = list(session.database.users_info.aggregate(most_played_categories_pipeline))

    # Convertir resultados a objetos Pydantic
    games = [Game(**game) for game in games_result]
    categories = [Category(**category) for category in categories_result]

    return games, categories
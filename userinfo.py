from typing import Tuple, List
from models.mongo_schema import Game, Category
from queries import dgraph_queries
import uuid
import connections
import bson

def get_most_played_stats(session, account_id: uuid.UUID):
    most_played_games_pipeline = [
        {
            "$match": {
                "userID": str(account_id)
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
                "gameID": "$game.gameID",
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
                "userID": str(account_id)
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

    games_result = list(session.database[connections.MONGODB_COLLECTION_NAME].aggregate(most_played_games_pipeline))
    categories_result = list(session.database[connections.MONGODB_COLLECTION_NAME].aggregate(most_played_categories_pipeline))

    # Convertir resultados a objetos Pydantic
    games = []
    categories = []
    for game in games_result:
        new_game = Game(gameID=game["gameID"], 
                        played_counter=game["played_counter"], 
                        time_playing=game["time_playing"],
                        category=game["category"])
        games.append(new_game)
    
    for category in categories_result:
        new_category = Category(category=category["category"], time_playing=category["time_playing"])
        categories.append(new_category)

    return games, categories

def cat(session_dgraph, categories):
    category_count = len(categories)

    recomendados = []
    if category_count == 0:
        result = dgraph_queries.all_games(session_dgraph, recomendados, 12)
        return result
    elif category_count == 1:
        cat1 = categories[0].category
        
        result_by_category = dgraph_queries.games_by_cat(session_dgraph, cat1, 6)
        result = dgraph_queries.all_games(session_dgraph, result_by_category, 6)
        return result
    elif category_count == 2:
        cat1 = categories[0].category
        
        cat2 = categories[1].category
        

        result_by_category1 = dgraph_queries.games_by_cat(session_dgraph, cat1, 6)
        
        result_by_category2 = dgraph_queries.games_by_cat(session_dgraph, cat2, 3)
        
        result_by_categories = result_by_category1 + result_by_category2
        result = dgraph_queries.all_games(session_dgraph, result_by_categories, 3)
        
        return result

    
def format_games(games):
    for i in range(len(games)):
        game = games[i]
        print("="*50)
        print("Opcion:", i+1)
        print("Game: "+game["j_name"])
        print("Description: "+game["description"])
        print("Category: "+game["category"]["c_name"])
        print("="*50)

def get_most_played_games(session, mpg):
    games = dgraph_queries.get_most_played_games(session, mpg)
    return games
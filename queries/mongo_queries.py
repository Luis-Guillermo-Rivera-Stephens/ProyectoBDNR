from typing import Optional
from models.mongo_schema import Game, Category, UserInfo
import uuid
from connections import MONGODB_COLLECTION_NAME
import bson

def update_stats(
    session,
    user_id,
    game_id,
    game_category,
    time_played,
    played_counter=1
):
    try:
        print("Updating stats")
        # Verificar y convertir user_id y game_id a uuid.UUID si es necesario
        user_id_binary = str(user_id)

        user_data = get_mongo_data(session, user_id_binary)
        if not user_data:
            return

        # Inicializar datos del usuario
        user = UserInfo(
            userID=user_data["userID"],
            TimePlaying=user_data["TimePlaying"],
            Games=user_data.get("Games", []),
            Categories=user_data.get("Categories", [])
        )

        # Actualizar tiempo de juego
        user.TimePlaying += time_played

        # Actualizar o agregar juego
        game_found = False
        for game in user.Games:
            if game.gameID == game_id:
                game.time_playing += time_played
                game.played_counter += played_counter
                game_found = True
                break

        if not game_found:
            new_game = Game(
                _gameID=game_id,
                played_counter=played_counter,
                time_playing=time_played,
                category=game_category
            )
            user.Games.append(new_game)

        # Actualizar o agregar categoría
        category_found = False
        for cat in user.Categories:
            if cat.category == game_category:
                cat.time_playing += time_played
                category_found = True
                break

        if not category_found:
            new_category = Category(
                category=game_category,
                time_playing=time_played
            )
            user.Categories.append(new_category)

        # Actualizar en MongoDB
        session.database[MONGODB_COLLECTION_NAME].update_one(
            {"userID": user_id_binary},
            {"$set": {
                "TimePlaying": user.TimePlaying,
                "Games": [game.dict(by_alias=True) for game in user.Games],
                "Categories": [cat.dict() for cat in user.Categories]
            }}
        )

        print("User updated")
        return True

    except Exception as e:
        print(f"Error updating user stats: {str(e)}")
        return False


def get_mongo_data(session, account_id_binary):
    try:
        # Buscar al usuario en la colección
        user_data = session.database[MONGODB_COLLECTION_NAME].find_one({"userID": account_id_binary})
        if not user_data:
            print(f"No se encontró usuario con userID: {account_id_binary}")
            return None
        print("Usuario encontrado:", user_data)
        return user_data
    except Exception as e:
        print(f"Error al obtener datos de MongoDB: {str(e)}")
        return None

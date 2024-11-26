from typing import Optional
from models.mongo_schema import Game, Category, UserInfo
import uuid
from connections import MONGODB_COLLECTION_NAME

def update_stats(
    session,
    user_id,
    game_id,
    game_category,
    time_played,
    played_counter = 1):
    try:
        user_data = session.database[MONGODB_COLLECTION_NAME].find_one({"userID": user_id})
        if not user_data:
            return False
        
        user = UserInfo(
            userID=user_data["userID"],
            TimePlaying=user_data["TimePlaying"],
            Games=user_data.get("Games", []), 
            Categories=user_data.get("Categories", [])
        )
        
        
        user.TimePlaying += time_played
        
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
            
        session.database[MONGODB_COLLECTION_NAME].update_one(
            {"userID": user_id},
            {"$set": {
                "TimePlaying": user.TimePlaying,
                "Games": [game.dict(by_alias=True) for game in user.Games],
                "Categories": [cat.dict() for cat in user.Categories]
            }}
        )
        
        return True
        
    except Exception as e:
        print(f"Error updating user stats: {str(e)}")
        return False
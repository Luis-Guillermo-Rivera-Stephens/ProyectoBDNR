from datetime import datetime
import uuid

def register_user(mongo_collection, username: str, password: str, admin_key: str = None):
    user_type = "admin" if admin_key == "specific_admin_key" else "player"
    if admin_key and user_type != "admin":
        return {"status": "error", "message": "Invalid admin key."}

    user = {
        "_id": str(uuid.uuid4()),
        "username": username,
        "password": password,  
        "user_type": user_type,
        "TimePlaying": 0,
        "Games": [],
        "Categories": []
    }
    mongo_collection.insert_one(user)
    return {"status": "success", "user_id": user["_id"]}

def start_game(mongo_collection, user_id: str, game_id: str, category: str):
    user = mongo_collection.find_one({"_id": user_id})
    if not user:
        return {"status": "error", "message": "User not found."}

    category_entry = next((cat for cat in user["Categories"] if cat["category"] == category), None)
    if not category_entry:
        user["Categories"].append({"category": category, "time_playing": 0})

    game_entry = {
        "_gameID": game_id,
        "played_counter": 1,
        "time_playing": 0,
        "category": category
    }
    user["Games"].append(game_entry)
    mongo_collection.update_one({"_id": user_id}, {"$set": {"Games": user["Games"], "Categories": user["Categories"]}})

    log_action(mongo_collection, user_id, f"Started game {game_id} in category {category}")
    return {"status": "success", "message": "Game started."}

def update_time_playing(mongo_collection, user_id: str, game_id: str, additional_time: int):
    user = mongo_collection.find_one({"_id": user_id})
    if not user:
        return {"status": "error", "message": "User not found."}

    for game in user["Games"]:
        if game["_gameID"] == game_id:
            game["time_playing"] += additional_time
            break

    for category in user["Categories"]:
        if category["category"] == game["category"]:
            category["time_playing"] += additional_time
            break

    user["TimePlaying"] += additional_time

    mongo_collection.update_one({"_id": user_id}, {"$set": user})
    log_action(mongo_collection, user_id, f"Updated playing time for game {game_id} by {additional_time} minutes.")
    return {"status": "success", "message": "Playing time updated."}

def log_action(mongo_collection, user_id: str, action: str):
    log_entry = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow()
    }
    mongo_collection.insert_one(log_entry)

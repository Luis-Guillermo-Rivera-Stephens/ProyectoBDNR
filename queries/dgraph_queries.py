#!/usr/bin/env python3
import os
import json
import random_choice

def all_games(client, recomendations, n):
    query = """
    {
        all_games(func: has(j_name)) {
            uid
            j_name
            description
            category {
                c_name
            }
        }
    }
    """
    txn = client.txn()
    try:
        res = txn.query(query)
        games = json.loads(res.json).get('all_games', [])

        random_games = random_choice.random_games(recomendations, games, n)
        return random_games

    finally:
        txn.discard()


def games_by_cat(client, category_name, n):
    query = """{{
    var(func: allofterms(c_name, "{0}")) {{
        uid_cat as uid
    }}

    games_by_cat(func: uid(uid_cat), first: {1}) {{
        c_name
        ~category {{
            uid
            j_name
            description
            category {{
                c_name
            }}
        }}
    }}
    }}"""
    txn = client.txn()
    try:
        res = txn.query(query.format(category_name, n))
        result = json.loads(res.json).get('games_by_cat', [])
        # Flatten the structure to match all_games format
        flattened_games = []
        for category in result:
            for game in category.get('~category', []):
                flattened_games.append(game)
        return flattened_games
    finally:
        txn.discard()

def get_all_games(client):
    query = """
    {
        all_games(func: has(j_name)) {
            uid
            j_name
            description
            category {
                c_name
            }
        }
    }
    """
    txn = client.txn()
    try:
        res = txn.query(query)
        games = json.loads(res.json).get('all_games', [])

        return games

    finally:
        txn.discard()
        return None
    
def get_most_played_games(client, mpg):
    # Construir la lista de UIDs para el query
    game_ids = [game.gameID for game in mpg]
    uids = ",".join(game_ids)
    
    query = """
    {
        games_by_ids(func: uid(%s)) {
            uid
            j_name
            description
            category {
                c_name
            }
        }
    }
    """ % uids

    txn = client.txn()
    try:
        res = txn.query(query)
        result = json.loads(res.json).get('games_by_ids', [])
        return result
    finally:
        txn.discard()
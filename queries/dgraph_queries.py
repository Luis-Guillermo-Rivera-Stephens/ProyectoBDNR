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


def games_by_cat(client,category_name, n):
    query = """
    {
    var(func: allofterms(c_name, "{}")) {
        uid_cat as uid
    }

    games_by_cat(func: uid(uid_cat), first:{}) {
        c_name
        ~category {
        uid
        j_name
        description
        }
    }
    }
    """
    txn = client.txn()
    try:
        res = txn.query(query.format(category_name, n))
        return json.loads(res.json).get('games_by_cat', []) 
    finally:
        txn.discard()

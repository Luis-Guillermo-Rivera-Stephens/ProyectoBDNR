#!/usr/bin/env python3
import os
import json
import random
import pydgraph

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')


def print_menu():
    mm_options = {
        1: "Get random games",
        2: "Get games by category (Tragamonedas)",
        3: "Exit"
    }
    for key in mm_options.keys():
        print(key, '--', mm_options[key])


def create_client_stub():
    return pydgraph.DgraphClientStub(DGRAPH_URI)


def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


def close_client_stub(client_stub):
    client_stub.close()


def jos_random(client):
    query = """
    {
        jos(func: has(j_name)) {
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
        # Convertir la respuesta JSON a un objeto de Python
        games = json.loads(res.json).get('jos', [])
        
        # Si hay menos de 6 juegos, devolver todos
        if len(games) <= 6:
            return games
        
        # Seleccionar 6 juegos aleatorios
        random_games = random.sample(games, 6)
        return random_games

    finally:
        txn.discard()


def memardo(client):
    query = """
    {
    var(func: allofterms(c_name, "Tragamonedas")) {
        uid_cat as uid
    }

    games_by_cat(func: uid(uid_cat)) {
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
        res = txn.query(query)
        return json.loads(res.json).get('games_by_cat', [])  # Devuelve la lista de juegos filtrados
    finally:
        txn.discard()


def main():
    client_stub = create_client_stub()
    client = create_client(client_stub)

    while True:
        print_menu()
        option = int(input('Enter your option: '))

        if option == 1:
            # Obtener juegos aleatorios
            try:
                games = jos_random(client)
                print(json.dumps(games, indent=2))  # Mostrar los juegos aleatorios
            except Exception as e:
                print(f"Error retrieving games: {e}")
        elif option == 2:
            # Obtener juegos por categoría "Tragamonedas"
            try:
                games_by_category = memardo(client)
                print(json.dumps(games_by_category, indent=2))  # Mostrar los juegos por categoría
            except Exception as e:
                print(f"Error retrieving games by category: {e}")
        elif option == 3:
            close_client_stub(client_stub)
            exit(0)
        else:
            print("Invalid option, please try again.")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')

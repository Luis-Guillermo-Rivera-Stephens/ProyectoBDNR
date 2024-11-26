import json
from ProyectoBDNR.schemas.dgraph_schema import set_schema
from pydgraph import DgraphClient, DgraphClientStub
from dgraph_model import Categoria, Juego


def connect_dgraph():
    stub = DgraphClientStub('localhost:9080')
    client = DgraphClient(stub)
    return client, stub


def populate_categories(client, categories):
    txn = client.txn()
    try:
        for category_data in categories:
            category = Categoria(**category_data)
            mutation = {
                "uid": "_:" + category._id,
                "dgraph.type": "Categoria",
                "_id": category._id,
                "name": category.name
            }
            txn.mutate(set_obj=mutation)
        txn.commit()
    finally:
        txn.discard()


def populate_games(client, games):
    txn = client.txn()
    try:
        for game_data in games:
            game = Juego(**game_data)
            mutation = {
                "uid": "_:" + game._id,
                "dgraph.type": "Juego",
                "_id": game._id,
                "name": game.name,
                "description": game.description,
                "category": f"_:{game.category}",
                "related_with": [f"_:{related_id}" for related_id in game.related_with]
            }
            txn.mutate(set_obj=mutation)
        txn.commit()
    finally:
        txn.discard()


def main():
    client, stub = connect_dgraph()
    set_schema(client)  
    with open('./populate_data/dgraph.json') as f:
        data = json.load(f)
    populate_categories(client, data['categories'])
    populate_games(client, data['juegos'])
    stub.close()

if __name__ == "__main__":
    main()

import json
import pydgraph
from models.dgraph_model import Categoria, Juego

def drop_all(client):
    client.alter(pydgraph.Operation(drop_all=True))

def populate_dgraph(client, data_path):
    """
    Función para popular Dgraph con datos desde un archivo JSON.
    """
    try:
        
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)

       
        txn = client.txn()

        try:
            
            mutation = pydgraph.Mutation(commit_now=True, set_json=json.dumps(data).encode("utf-8"))
            response = txn.mutate(mutation)
            print("Datos insertados correctamente.")
            print(f"UIDs creados: {response.uids}")

        except Exception as e:
            print(f"Error durante la mutación: {e}")
            txn.discard()
        finally:
            txn.discard()

    except FileNotFoundError:
        print(f"Archivo no encontrado: {data_path}")
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON.")


if __name__ == "__main__":
    # Conectar a Dgraph
    stub = pydgraph.DgraphClientStub("localhost:9080")
    client = pydgraph.DgraphClient(stub)

    try:
        drop_all(client)
        print("Esquema y datos eliminados (DROP ALL).")
        
        from schemas.dgraph_schema import set_schema
        set_schema(client)

        
        data_path = "./populate_data/dgraph.json"
        populate_dgraph(client, data_path)

    finally:
        
        stub.close()

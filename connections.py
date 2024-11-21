import os
from cassandra.cluster import Cluster
from pymongo import MongoClient
import pydgraph

CASSANDRA_CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
CASSANDRA_KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'app')
CASSANDRA_REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGO_DB_NAME = os.getenv('MONGODB_DB_NAME', 'proyecto')
MONGODB_COLLECTION_NAME = os.getenv('MONGODB_COLLECTION_NAME', 'stats')

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def cassandra_connection():
    cluster = Cluster(CASSANDRA_CLUSTER_IPS.split(','))
    session = cluster.connect()
    session.set_keyspace(CASSANDRA_KEYSPACE)
    return session

def mongodb_connection():
    client = MongoClient(MONGODB_URI)
    db = client[MONGO_DB_NAME]
    collection = db[MONGODB_COLLECTION_NAME]
    return client, collection

def dgraph_connection():
    client_stub = pydgraph.DgraphClientStub(DGRAPH_URI)
    client = pydgraph.DgraphClient(client_stub)
    return client_stub, client

def close_all_connections(cassandra_session, mongo_client, dgraph_client_stub):
    cassandra_session.shutdown()
    mongo_client.close()
    dgraph_client_stub.close()
    print("Todas las conexiones han sido cerradas.")

cassandra_session = cassandra_connection()
mongo_client, mongo_collection = mongodb_connection()

dgraph_client_stub, dgraph_client = dgraph_connection()
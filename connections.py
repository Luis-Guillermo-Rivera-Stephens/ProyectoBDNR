import os
from cassandra.cluster import Cluster
from pymongo import MongoClient
import pydgraph

from schemas import cassandra_schema

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
    cassandra_schema.create_keyspace(session, CASSANDRA_KEYSPACE, CASSANDRA_REPLICATION_FACTOR)
    cassandra_schema.set_keyspace(session, CASSANDRA_KEYSPACE)
    cassandra_schema.set_schema(session)
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

Cassandra_session = cassandra_connection()
Mongo_client, Mongo_collection = mongodb_connection()

Dgraph_client_stub, Dgraph_client = dgraph_connection()
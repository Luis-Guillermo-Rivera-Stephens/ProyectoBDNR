import uuid
import datetime
import connections 
from queries import cassandra_queries
import json
from models import mongo_schema
from bson import Binary

def read_data_from_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def mongo_creation(session ,user_id):
    newuser = mongo_schema.UserInfo(
    userID= str(user_id),  
    TimePlaying=0,   
    Games=[],
    Categories=[])
    newuser_dict = newuser.dict(by_alias=True)
    newuser_dict['userID'] = str(user_id)

    # Insertar en MongoDB
    session.database[connections.MONGODB_COLLECTION_NAME].insert_one(newuser_dict)


def populate_administrators(session, administrators):
    query = session.prepare(cassandra_queries.CASSANDRA_REGISTER_ADMIN_QUERY)
    for admin in administrators:
        admin_id = uuid.uuid4()
        username = admin["username"]
        password = admin["password"]
        key = admin["key"]
        creation_date = datetime.datetime.now()
        charge = admin["charge"]

        session.execute(
            query,
            (admin_id, username, password, key, creation_date, charge)
        )
        username_reg = session.prepare(cassandra_queries.CASSANDRA_REGISTER_USERNAME_QUERY)
        session.execute(username_reg, (admin_id, username, True))

def create_log(session, account_id):
    log_time = datetime.datetime.now()
    default_game_id = uuid.UUID("00000000-0000-0000-0000-000000000000")
    for tablename in cassandra_queries.CASSANDRA_LOG_TABLES_NAME:
        query = session.prepare(cassandra_queries.CASSANDRA_LOG_QUERY.format(tablename))
        session.execute(query, (account_id, default_game_id, "User created", log_time, log_time))
        
def populate_users(session_cass, session_mongo, users):
    print(users)
    query1 =  session_cass.prepare(cassandra_queries.CASSANDRA_REGISTER_ACCOUNT_QUERY)
    query2 = session_cass.prepare(cassandra_queries.CASSANDRA_REGISTER_ACCOUNT_ID_QUERY)
    for user in users:
        account_id = uuid.uuid4()
        username = user["username"]
        password = user["password"]
        creation_date = datetime.datetime.now()
        print("New user: ", account_id, username, password, creation_date)
        print("Query 1")
        session_cass.execute(
            query1,
            (account_id, username, password, creation_date)
        )
        print("Query 2")
        session_cass.execute(
            query2,
            (account_id, username, password, creation_date)
        )
        create_log(session_cass, account_id)
        mongo_creation(session_mongo, account_id)

        username_reg = session_cass.prepare(cassandra_queries.CASSANDRA_REGISTER_USERNAME_QUERY)
        session_cass.execute(username_reg, (account_id, username, False))


def clear_cassandra_database(session):
    for table in cassandra_queries.CASSANDRA_ALL_TABLES:
        query = f"TRUNCATE {table}"
        session.execute(query)

def clear_mongodb_database(session):
    session.database[connections.MONGODB_COLLECTION_NAME].delete_many({})

def main():
    file_path = "./populate_data/cassandra_data.json"
    data = read_data_from_json(file_path)

    administrators = data["administrators"]
    users = data["users"]

    flag = input("deseas eliminar toda la data antes de hacer el populate? (y/n): ")
    
    session_cass = connections.Cassandra_session
    session_mongo = connections.Mongo_client
    
    if flag == "y":
        clear_cassandra_database(session_cass)
        clear_mongodb_database(session_mongo)


    populate_administrators(session_cass, administrators)
    populate_users(session_cass, session_mongo, users)




if __name__ == "__main__":
    main()

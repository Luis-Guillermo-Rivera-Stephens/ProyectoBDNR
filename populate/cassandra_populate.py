import uuid
import datetime
from ..connections import Cassandra_session
from ..queries import cassandra_queries
import json

def read_data_from_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

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

def populate_users(session, users):
    query =  session.prepare(cassandra_queries.CASSANDRA_REGISTER_ACCOUNT_QUERY)
    for user in users:
        account_id = uuid.uuid4()
        username = user["username"]
        password = user["password"]
        creation_date = datetime.datetime.now()


        session.execute(
            query,
            (account_id, username, password, creation_date,
             account_id, username, password, creation_date)
        )
        create_log(session, account_id)


def create_log(session, account_id):
    log_time = datetime.datetime.now()

    for tablename in cassandra_queries.CASSANDRA_LOG_TABLES_NAME:
        query = session.prepare(cassandra_queries.CASSANDRA_LOG_QUERY.format(tablename))
        session.execute(query, (account_id, None, "User created", log_time, log_time))

def main():
    file_path = "./cassandra_data.json"
    data = read_data_from_json(file_path)

    administrators = data["administrators"]
    users = data["users"]

    session = Cassandra_session
    populate_administrators(session, administrators)
    populate_users(session, users)


if __name__ == "__main__":
    main()

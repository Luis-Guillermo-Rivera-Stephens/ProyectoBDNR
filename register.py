import login
from queries.cassandra_queries import CASSANDRA_REGISTER_QUERY
import uuid
from datetime import datetime, timezone
from models import mongo_schema
import connections

def mongo_creation(session ,user_id):
    newuser = mongo_schema.UsersInfo(user_id, 0, [], [])
    session.database[connections.MONGODB_COLLECTION_NAME].insert_one(newuser.dict(by_alias=True))

def register(session,username, password):
    try: 
        account_id = uuid.uuid4()
        creation_date = datetime.now(timezone.utc)

        query = session.prepare(CASSANDRA_REGISTER_QUERY)
        session.execute(query, [account_id, username, password, creation_date])
        

    except Exception as e:
        print(f"Error registering user: {e}")
        return False
    
    result = login.login(username, password)
    if result is None: 
        return False
    else:
        return result



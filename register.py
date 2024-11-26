import login
from queries.cassandra_queries import CASSANDRA_REGISTER_ACCOUNT_QUERY, CASSANDRA_REGISTER_ACCOUNT_ID_QUERY
import uuid
from datetime import datetime, timezone
from models import mongo_schema
import connections
import exist

def mongo_creation(session ,user_id):
    newuser = mongo_schema.UsersInfo(user_id, 0, [], [])
    session.database[connections.MONGODB_COLLECTION_NAME].insert_one(newuser.dict(by_alias=True))

def register_user(session,username, password):
    try: 
        flag, usernameRes = exist.username_exist(session, username) 
        if flag:
            return None, f"Username {usernameRes.username} is already registered"
        
        account_id = uuid.uuid4()
        creation_date = datetime.now(timezone.utc)

        query1 = session.prepare(CASSANDRA_REGISTER_ACCOUNT_QUERY)
        query2 = session.prepare(CASSANDRA_REGISTER_ACCOUNT_ID_QUERY)
        session.execute(query1, [account_id, username, password, creation_date])
        session.execute(query2, [account_id, username, password, creation_date])
        

    except Exception as e:
        print(f"Error registering user: {e}")
        return False
    
    result = login.login(username, password)
    if result is None: 
        return False
    else:
        return result



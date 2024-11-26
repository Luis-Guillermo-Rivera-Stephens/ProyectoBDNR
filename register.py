import login
from queries.cassandra_queries import CASSANDRA_REGISTER_ACCOUNT_QUERY, CASSANDRA_REGISTER_ACCOUNT_ID_QUERY, CASSANDRA_REGISTER_ADMIN_QUERY, CASSANDRA_REGISTER_USERNAME_QUERY
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
        username_query = session.prepare(CASSANDRA_REGISTER_USERNAME_QUERY)

        session.execute(query1, [account_id, username, password, creation_date])
        session.execute(query2, [account_id, username, password, creation_date])
        session.execute(username_query, [account_id, username, False])
        

    except Exception as e:
        return None, f"Error registering user: {e}"
    
    return True, f"User {username} registered"

def register_admin(session, username, password, charge):
        try: 
            flag, usernameRes = exist.username_exist(session, username) 
            if flag:
                return None, f"Username {usernameRes.username} is already registered"
        
            account_id = uuid.uuid4()
            creation_date = datetime.now(timezone.utc)

            query1 = session.prepare(CASSANDRA_REGISTER_ADMIN_QUERY)
            username_query = session.prepare(CASSANDRA_REGISTER_USERNAME_QUERY)
            session.execute(query1, [account_id, username, password, "shared_key" ,creation_date, charge])
            session.execute(username_query, [account_id, username, True])
            

        except Exception as e:
            return None, f"Error registering user: {e}"
    
        return True, f"User {username} registered"

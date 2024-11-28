
from queries.cassandra_queries import CASSANDRA_REGISTER_ACCOUNT_QUERY, CASSANDRA_REGISTER_ACCOUNT_ID_QUERY, CASSANDRA_REGISTER_ADMIN_QUERY, CASSANDRA_REGISTER_USERNAME_QUERY
import uuid
from datetime import datetime, timezone
from models import mongo_schema
import connections
import exist
import log_creation
import bson
def mongo_creation(session ,user_id):
    newuser = mongo_schema.UserInfo(
        userID=user_id,
        TimePlaying=0,
        Games=[],
        Categories=[]
    )
    session.database[connections.MONGODB_COLLECTION_NAME].insert_one(newuser.dict(by_alias=True))

def register_user(session, mongo_session, username, password):
    if verify_info(username, password) == False:
        return None, "Campos invalidos"
    try: 
        flag, usernameRes = exist.username_exist(session, username) 
        if flag:
            return None, f"Username {usernameRes.username} is already registered"
        
        account_id = str(uuid.uuid4())
        creation_date = datetime.now()


        query1 = session.prepare(CASSANDRA_REGISTER_ACCOUNT_QUERY)
        query2 = session.prepare(CASSANDRA_REGISTER_ACCOUNT_ID_QUERY)
        username_query = session.prepare(CASSANDRA_REGISTER_USERNAME_QUERY)

        session.execute(query1, [account_id, username, password, creation_date])
        session.execute(query2, [account_id, username, password, creation_date])
        session.execute(username_query, [account_id, username, False])
        

    except Exception as e:
        return None, f"Error registering user: {e}"
    
    mongo_creation(mongo_session, account_id)
    log_creation.log_creation(session, account_id,  str(uuid.UUID("00000000-0000-0000-0000-000000000000")), "Usuario creado", creation_date, creation_date)


    return True, f"User {username} registered"


def register_admin(session, username, password, charge):
    if verify_info(username, password) == False:
        return None, "Campos invalidos"
    try: 
        flag, usernameRes = exist.username_exist(session, username) 
        if flag:
            return None, f"Username {usernameRes.username} is already registered"
    
        admin_id = str(uuid.uuid4())
        creation_date = datetime.now(timezone.utc)

        query1 = session.prepare(CASSANDRA_REGISTER_ADMIN_QUERY)
        username_query = session.prepare(CASSANDRA_REGISTER_USERNAME_QUERY)
        
        session.execute(query1, [admin_id, username, password, "shared_key", creation_date, charge])
        session.execute(username_query, [admin_id, username, True])

    except Exception as e:
        return None, f"Error registering user: {e}"

    return True, f"User {username} registered"

def verify_info(username, password):
    return len(username) > 0 and len(password) > 0



from queries.cassandra_queries import CASSANDRA_REGISTER_ACCOUNT_QUERY, CASSANDRA_REGISTER_ACCOUNT_ID_QUERY, CASSANDRA_REGISTER_ADMIN_QUERY, CASSANDRA_REGISTER_USERNAME_QUERY
import uuid
from datetime import datetime, timezone
from models import mongo_schema
import connections
import exist

from models import account_model, administrator_model

def mongo_creation(session ,user_id):
    newuser = mongo_schema.UsersInfo(user_id, 0, [], [])
    session.database[connections.MONGODB_COLLECTION_NAME].insert_one(newuser.dict(by_alias=True))

def register_user(session,username, password):
    if verify_info(username, password) == False:
        return None, "Campos invalidos"
    try: 
        flag, usernameRes = exist.username_exist(session, username) 
        if flag:
            return None, f"Username {usernameRes.username} is already registered"
        
        account_id = uuid.uuid4()
        creation_date = datetime.now(timezone.utc)

        try:
            account = account_model.ACCOUNT(account_id, username, password, creation_date)
        except Exception as e:
            return None, f"Error creating user: {str(e)}"

        query1 = session.prepare(CASSANDRA_REGISTER_ACCOUNT_QUERY)
        query2 = session.prepare(CASSANDRA_REGISTER_ACCOUNT_ID_QUERY)
        username_query = session.prepare(CASSANDRA_REGISTER_USERNAME_QUERY)

        session.execute(query1, [account_id, username, password, creation_date])
        session.execute(query2, [account_id, username, password, creation_date])
        session.execute(username_query, [account_id, username, False])
        

    except Exception as e:
        return None, f"Error registering user: {e}"
    
    return True, f"User {username} registered"

def register_user(session, username, password):
    if verify_info(username, password) == False:
        return None, "Campos invalidos"
    try: 
        flag, usernameRes = exist.username_exist(session, username) 
        if flag:
            return None, f"Username {usernameRes.username} is already registered"
        
        account_id = uuid.uuid4()
        creation_date = datetime.now(timezone.utc)

        try:
            account = account_model.ACCOUNT(
                account_id=account_id,  # o _account_id según el alias
                username=username,
                password=password,
                creation_date=creation_date
            )
        except Exception as e:
            return None, f"Error creating user: {str(e)}"

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
    if verify_info(username, password) == False:
        return None, "Campos invalidos"
    try: 
        flag, usernameRes = exist.username_exist(session, username) 
        if flag:
            return None, f"Username {usernameRes.username} is already registered"
    
        admin_id = uuid.uuid4()
        creation_date = datetime.now(timezone.utc)

        try:
            admin = administrator_model.ADMIN(
                admin_id=admin_id,  # o _admin_id según el alias
                username=username,
                password=password,
                key="shared_key",
                creation_date=creation_date,
                charge=charge
            )
        except Exception as e:
            return None, f"Error registering admin: {e}"

        query1 = session.prepare(CASSANDRA_REGISTER_ADMIN_QUERY)
        username_query = session.prepare(CASSANDRA_REGISTER_USERNAME_QUERY)
        
        # Aquí hay un error, estás pasando el objeto admin completo
        # Deberías pasar los valores individuales
        session.execute(query1, [admin_id, username, password, "shared_key", creation_date, charge])
        session.execute(username_query, [admin_id, username, True])

    except Exception as e:
        return None, f"Error registering user: {e}"

    return True, f"User {username} registered"
def verify_info(username, password):
    return len(username) > 0 and len(password) > 0

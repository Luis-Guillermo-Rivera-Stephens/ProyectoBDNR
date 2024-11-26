from queries.cassandra_queries import CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY, CASSANDRA_USERNAMES_MIDDLEWARE, CASSANDRA_LOGIN_ADMIN_QUERY
import exist
from models import administrator_model, account_model

def login(session, username, password, key = None):
    print("Login")
    flag, usernameRes = exist.username_exist(session, username)
    print(usernameRes)
    print("Flag de login: ", flag)

    if flag == False:
        return None, False, "No existe el usuario"
    
    if usernameRes.admin:
        query = session.prepare(CASSANDRA_LOGIN_ADMIN_QUERY)
        admin = True
    else:
        query = session.prepare(CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY)
        admin = False
   
    result = session.execute(query, (username,))[0]
    if result.password != password:
        return None, False, "Password incorrecto"
    if usernameRes.admin and result.key != key:
        return None, False, "Llave compartida incorrecta"
    
    if admin:
        admin_obj = administrator_model.ADMIN(
            admin_id=result.admin_id,
            username=result.username,
            password=result.password,
            key=result.key,
            creation_date=result.creation_date,
            charge=result.charge
        )
        return admin_obj, admin, "Usuario logeado"
    else:
        account_obj = account_model.ACCOUNT(
            account_id=result.account_id,
            username=result.username,
            password=result.password,
            creation_date=result.creation_date
        )
        return account_obj, admin, "Usuario logeado"
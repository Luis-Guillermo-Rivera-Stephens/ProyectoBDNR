from queries.cassandra_queries import CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY, CASSANDRA_USERNAMES_MIDDLEWARE, CASSANDRA_LOGIN_ADMIN_QUERY
import exist

def login(session, username, password, key = None):

    flag, usernameRes = exist.username_exist(session, username)
    print(usernameRes)
    print("Flag: ", flag)

    if flag == False:
        return None, False, "No existe el usuario"
    
    if usernameRes.admin:
        query = session.prepare(CASSANDRA_LOGIN_ADMIN_QUERY)
        admin = True
        
    else:
         query = session.prepare(CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY)
         admin = False
   
    
    result = session.execute(query, (username,))
    if result[0].password != password:
        return None, False, "Password incorrecto"
    if usernameRes.admin and result[0].key != key:
        return None, False, "Llave compartida incorrecta"
    

    return result[0], admin, "Usuario logeado"
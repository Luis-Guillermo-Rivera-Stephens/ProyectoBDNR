from queries.cassandra_queries import CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY, CASSANDRA_USERNAMES_MIDDLEWARE, CASSANDRA_LOGIN_ADMIN_QUERY
import exist

def login(session, username, password, key = None):

    flag, usernameRes = exist.username_exist(session, username)

    if not flag:
        return None
    
    if usernameRes.admin:
        query = session.prepare(CASSANDRA_LOGIN_ADMIN_QUERY)
        admin = True
        
    else:
         query = session.prepare(CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY)
         admin = False
   
    
    result = session.execute(query, (username,))
    if result[0].password != password:
        return None
    if usernameRes.admin and result[0].key != key:
        return None
    

    return result[0], admin
from queries.cassandra_queries import CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY, CASSANDRA_USERNAMES_MIDDLEWARE, CASSANDRA_LOGIN_ADMIN_QUERY

def login(session, username, password, key = None):

    query_middle = session.prepare(CASSANDRA_USERNAMES_MIDDLEWARE)
    username = session.execute(query_middle, (username))

    if len(username) == 0:
        return None
    
    if username[0].admin:
        query = session.prepare(CASSANDRA_LOGIN_ADMIN_QUERY)
        admin = True
        if result[0].key != key:
            return None
        
    else:
         query = session.prepare(CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY)
         admin = False
   
    result = session.execute(query, (username))
    if result[0].password != password:
        return None
    

    return result[0], admin
from queries.cassandra_queries import CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY, CASSANDRA_USERNAMES_MIDDLEWARE, CASSANDRA_LOGIN_ADMIN_QUERY

def username_exist(session, username):

    query_middle = session.prepare(CASSANDRA_USERNAMES_MIDDLEWARE)
    username = session.execute(query_middle, (username))

    if len(username) == 0:
        return False, None
    
    return True, username 

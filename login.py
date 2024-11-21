from queries.cassandra_queries import CASSANDRA_LOGIN_QUERY

def login(session, username, password):
    query = session.prepare(CASSANDRA_LOGIN_QUERY)
    result = session.execute(query, [username])
    if len(result) == 0:
        return None
    
    account = result[0]
    if account.password != password:
        return None
    
    return account
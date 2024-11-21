CASSANDRA_LOGIN_QUERY = """
    SELECT * 
    FROM ACCOUNTS_BY_USER
    WHERE username = ?
"""

CASSANDRA_REGISTER_QUERY = """
    INSERT INTO ACCOUNTS_BY_USER (account_id, username, password, creation_date)
    VALUES (?, ?, ?, ?)
"""

CASSANDRA_LOG_QUERY = """
    INSERT INTO {} (account_id, game_id, description, start, end)
    VALUES (?, ?, ?, ?, ?)
"""

CASSANDRA_LOG_TABLES_NAME = ["LOGS_BY_USER", "LOGS_BY_USER_DATERANGE", "LOGS_BY_USER_GAME", 
                          "LOGS_BY_USER_GAME_DATERANGE", "LOGS_BY_GAME", "LOGS_BY_GAME_DATERANGE"]

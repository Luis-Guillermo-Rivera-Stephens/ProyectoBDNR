CASSANDRA_LOGIN_ACCOUNT_BY_USER_QUERY = """
    SELECT * 
    FROM ACCOUNTS_BY_USER
    WHERE username = ?
"""

CASSANDRA_LOGIN_ACCOUNT_BY_ID_QUERY = """
    SELECT * 
    FROM ACCOUNTS_BY_ID
    WHERE account_id = ?
"""

CASSANDRA_LOGIN_ADMIN_QUERY = """
    SELECT * 
    FROM ADMINISTRATOR_BY_USER
    WHERE username = ?
"""

CASSANDRA_USERNAMES_MIDDLEWARE = """
    SELECT * 
    FROM USERNAMES
    WHERE username = ?
"""


CASSANDRA_REGISTER_ACCOUNT_QUERY = """
    INSERT INTO ACCOUNTS_BY_USER (account_id, username, password, creation_date)
    VALUES (?, ?, ?, ?);
"""
CASSANDRA_REGISTER_ACCOUNT_ID_QUERY = """
    INSERT INTO  ACCOUNTS_BY_ID (account_id, username, password, creation_date)
    VALUES (?, ?, ?, ?);
"""

CASSANDRA_REGISTER_ADMIN_QUERY = """
    INSERT INTO ADMINISTRATOR_BY_USER (admin_id, username, password, key, creation_date, charge)
    VALUES (?, ?, ?, ?, ?, ?)
"""

CASSANDRA_LOG_QUERY = """
    INSERT INTO {} (account_id, game_id, description, start, end)
    VALUES (?, ?, ?, ?, ?)
"""

CASSANDRA_LOG_TABLES_NAME = ["LOGS_BY_USER", "LOGS_BY_USER_DATERANGE", "LOGS_BY_USER_GAME", 
                          "LOGS_BY_USER_GAME_DATERANGE", "LOGS_BY_GAME", "LOGS_BY_GAME_DATERANGE"]
DATE_RANGE = """
    AND trade_id > minTimeuuid(?)
    AND trade_id < maxtimeuuid(?)
"""

CASSANDRA_ALL_TABLES = ["USERNAMES", "ACCOUNTS_BY_USER", "ACCOUNTS_BY_ID", "ADMINISTRATOR_BY_USER","LOGS_BY_USER", "LOGS_BY_USER_DATERANGE", "LOGS_BY_USER_GAME", 
                          "LOGS_BY_USER_GAME_DATERANGE", "LOGS_BY_GAME", "LOGS_BY_GAME_DATERANGE"]
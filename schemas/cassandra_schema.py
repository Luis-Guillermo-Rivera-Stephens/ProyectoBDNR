from cassandra.cluster import Cluster

CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

ACCOUNTS_BY_USER_TABLE = """
        CREATE TABLE IF NOT EXISTS ACCOUNTS_BY_USER (
                account_id TEXT,
                username TEXT,
                password TEXT,
                creation_date TIMESTAMP,
                PRIMARY KEY (username)
        )
"""
ACCOUNTS_BY_ID_TABLE = """
        CREATE TABLE IF NOT EXISTS ACCOUNTS_BY_ID (
                account_id TEXT,
                username TEXT,
                password TEXT,
                creation_date TIMESTAMP,
                PRIMARY KEY (account_id)
        )
"""

ADMINISTRATOR_TABLE = """
        CREATE TABLE IF NOT EXISTS ADMINISTRATOR_BY_USER (
                admin_id TEXT,
                username TEXT,
                password TEXT,
                key text,
                creation_date TIMESTAMP,
                charge TEXT,
                PRIMARY KEY (username)
        )
"""

USERNAMES = """
        CREATE TABLE IF NOT EXISTS USERNAMES (
                id TEXT,
                username TEXT,
                admin BOOLEAN,
                PRIMARY KEY (username)
        )
"""

LOGS_BY_USER = """
        CREATE TABLE IF NOT EXISTS LOGS_BY_USER (
                account_id TEXT,
                game_id TEXT,
                description TEXT,
                start TIMESTAMP,
                end TIMESTAMP,
                PRIMARY KEY (account_id, game_id)
        )
"""

LOGS_BY_USER_DATERANGE = """
        CREATE TABLE IF NOT EXISTS LOGS_BY_USER_DATERANGE (
                account_id TEXT,
                game_id TEXT,
                description TEXT,
                start TIMESTAMP,
                end TIMESTAMP,
                PRIMARY KEY (account_id, start, end)
        )
"""

LOGS_BY_USER_GAME = """
        CREATE TABLE IF NOT EXISTS LOGS_BY_USER_GAME (
                account_id TEXT,
                game_id TEXT,
                description TEXT,
                start TIMESTAMP,
                end TIMESTAMP,
                PRIMARY KEY (account_id, game_id)
        )
"""

LOGS_BY_USER_GAME_DATERANGE = """
        CREATE TABLE IF NOT EXISTS LOGS_BY_USER_GAME_DATERANGE (
                account_id TEXT,
                game_id TEXT,
                description TEXT,
                start TIMESTAMP,
                end TIMESTAMP,
                PRIMARY KEY (account_id, game_id, start, end)
        )
"""

LOGS_BY_GAME = """
        CREATE TABLE IF NOT EXISTS LOGS_BY_GAME (
                account_id TEXT,
                game_id TEXT,
                description TEXT,
                start TIMESTAMP,
                end TIMESTAMP,
                PRIMARY KEY (game_id)
        )
"""

LOGS_BY_GAME_DATERANGE = """
        CREATE TABLE IF NOT EXISTS LOGS_BY_GAME_DATERANGE (
                account_id TEXT,
                game_id TEXT,
                description TEXT,
                start TIMESTAMP,
                end TIMESTAMP,
                PRIMARY KEY (game_id, start, end)
        )
"""

def create_keyspace(session, keyspace, replication_factor):
    print(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def set_keyspace(session, keyspace):
    session.execute(f"USE {keyspace}")

def set_schema(session):
    session.execute(USERNAMES)
    session.execute(ACCOUNTS_BY_USER_TABLE)
    session.execute(ACCOUNTS_BY_ID_TABLE)
    session.execute(ADMINISTRATOR_TABLE)
    session.execute(LOGS_BY_USER)
    session.execute(LOGS_BY_USER_GAME)
    session.execute(LOGS_BY_USER_DATERANGE)
    session.execute(LOGS_BY_USER_GAME_DATERANGE)
    session.execute(LOGS_BY_GAME)
    session.execute(LOGS_BY_GAME_DATERANGE)


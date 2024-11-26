from queries.cassandra_queries import CASSANDRA_LOG_QUERY as QUERY, CASSANDRA_LOG_TABLES_NAME as TABLES
import uuid
import datetime

def log_creation(session, id_account, game_id, description, start_date, end_date):
    verif_info_ = verif_info(id_account, game_id, description, start_date, end_date)
    
    if not verif_info_:
        return False

    for table in TABLES:
        query = session.prepare(QUERY.format(table))
        session.execute(query, (id_account, game_id, description, start_date, end_date))

def verif_info(id_account, game_id, description, start_date, end_date):
    if not isinstance(id_account, uuid.UUID) and not isinstance(game_id, uuid.UUID):
        return False
    if len(description) == 0:
        return False

    if start_date > end_date:
        return False
    
    return True



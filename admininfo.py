from queries.cassandra_queries import (
    CASSANDRA_LOG_QUERY,
    CASSANDRA_LOG_TABLES_NAME,
)

def get_logs_by_user(session, account_id):
    if not account_id:
        raise ValueError("Error: account_id no proporcionado o no válido.")
    
    print(f"Consultando logs para account_id: {account_id}")

    logs = []
    for table in CASSANDRA_LOG_TABLES_NAME:
        try:
            if "GAME" in table and "DATERANGE" not in table:
                # Tablas que requieren game_id
                print(f"Saltando tabla {table} porque falta game_id.")
                continue
            if "DATERANGE" in table:
                # Tablas que requieren rango de fechas
                print(f"Saltando tabla {table} porque falta rango de fechas.")
                continue
            
            print(f"Ejecutando consulta en tabla: {table} con account_id: {account_id}")
            query = session.prepare(CASSANDRA_LOG_QUERY.format(table))
            result = session.execute(query, (account_id,))
            logs.extend(result)
        except Exception as e:
            print(f"Error al ejecutar la consulta en tabla {table}: {e}")
            continue
    
    return logs


def get_logs_by_game(session, game_id):
    if not game_id:
        raise ValueError("Error: game_id no proporcionado o no válido.")
    
    print(f"Consultando logs para game_id: {game_id}")

    logs = []
    for table in CASSANDRA_LOG_TABLES_NAME:
        try:
            if "USER" in table and "DATERANGE" not in table:
                # Tablas que requieren account_id, no game_id
                print(f"Saltando tabla {table} porque falta account_id.")
                continue
            if "DATERANGE" in table:
                # Tablas que requieren rango de fechas
                print(f"Saltando tabla {table} porque falta rango de fechas.")
                continue
            
            print(f"Ejecutando consulta en tabla: {table} con game_id: {game_id}")
            query = session.prepare(CASSANDRA_LOG_QUERY.format(table))
            result = session.execute(query, (game_id,))
            logs.extend(result)
        except Exception as e:
            print(f"Error al ejecutar la consulta en tabla {table}: {e}")
            continue
    
    return logs



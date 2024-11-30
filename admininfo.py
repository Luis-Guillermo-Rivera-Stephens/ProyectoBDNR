import queries.cassandra_queries as q
import queries.dgraph_queries as d
import connections
import models.logs_model as LOG

import datetime

def get_logs_by_user(session = connections.Cassandra_session):
    print("get_logs_by_user")
    account_id = get_user_account(session)
    flag = input("Quieres filtrar por juego? (y/n): ")
    flag = flag.lower() == "y" 

    if flag:
        game_id = get_game_id()
        query = q.LOG_BY_USER_GAME_QUERY
    else:
        query = q.LOG_BY_USER_QUERY

    date_flag = input("Quieres establecer un rango de fechas (y/n): ")
    date_flag = date_flag.lower() == "y" 
    if date_flag:
        start, end = stablish_a_daterange()
        query = query+q.DATE_RANGE

    query = session.prepare(query)
    if flag and date_flag:
        result = session.execute(query, (account_id, game_id, start, end))
    elif flag and not date_flag:
        result = session.execute(query, (account_id, game_id))
    elif not flag and date_flag:
        result = session.execute(query, (account_id, start, end))
    else:
        result = session.execute(query, (account_id,))
    format_logs(result)
    
def get_logs_by_game(session):
    game_id = get_game_id()  
    query = "SELECT * FROM LOGS_BY_GAME WHERE game_id = ?"  

    
    date_flag = input("Quieres establecer un rango de fechas (y/n): ").lower() == "y"
    if date_flag:
        start, end = stablish_a_daterange()
        query += " AND start >= ? AND start <= ?"

   
    print(f"Consulta a ejecutar: {query}")

    try:
        query = session.prepare(query)  

        
        if date_flag:
            result = session.execute(query, (game_id, start, end))
        else:
            result = session.execute(query, (game_id,))
        
        format_logs(result)
    except Exception as e:
        print(f"Error ejecutando la consulta: {e}")


    


def get_user_account(session):
    print("Consultando todos los usuarios")
    result = session.execute(q.CASSANDRA_GET_ALL_ACCOUNTS)
    
    print("\nUsuarios disponibles:")
    print("=" * 50)
    for row in result:
        print(f"ID: {row.account_id}")
        print(f"Usuario: {row.username}")
        print("-" * 50)
    
    return input("Enter the id: ")

def stablish_a_daterange():
    print("Estableciendo rango de fechas")
    start_day = datetime.datetime.strptime(input("Start Day (yyyy-MM-dd): "), "%Y-%m-%d").date()
    end_day = datetime.datetime.strptime(input("End Day (yyyy-MM-dd): "), "%Y-%m-%d").date()
    return start_day, end_day

def get_game_id(session = connections.Dgraph_client):
    print("Consultando todos los juegos")

    result = d.get_all_games(session)
    print(result)
    return input("Inserta el uid del juego: ")

    
def format_logs(result):
    print("\nRegistros de juegos por usuario:")
    print("=" * 80)
    
    for row in result:
        log = LOG.LOG(
            account_id=row.account_id,
            game_id=row.game_id,
            description=row.description,
            start=row.start,
            end=row.end
        )
        print("_"*50)
        print(f"ID: {log.account_id}")
        print(f"Juego: {log.game_id}")
        print(f"Descripción: {log.description}")
        print(f"Fecha de inicio: {log.start}")
        print(f"Fecha de fin: {log.end}")
        print("-" * 50)

    
    print("=" * 80)
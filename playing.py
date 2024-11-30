import datetime
from queries import mongo_queries
import log_creation
import connections


def playing(mongo_session, id_account, game_id, category):
    start_time = datetime.datetime.now()
    print("Jugando ...")
    input("Presiona Enter para terminar")
    end_time = datetime.datetime.now()

    elapsed_time = round((end_time - start_time).total_seconds())
    print("Tiempo de juego en segundos:", elapsed_time)
    if elapsed_time > 0:
        print("Elapsed time:", elapsed_time)
        mongo_queries.update_stats(mongo_session, id_account,game_id, category, elapsed_time)
        log_creation.log_creation(connections.Cassandra_session, id_account, game_id, f"user played {game_id} for {elapsed_time} seconds", start_time, end_time)


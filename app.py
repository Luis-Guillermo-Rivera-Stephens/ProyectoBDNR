from admininfo import get_logs_by_game, get_logs_by_user
import login 
import register 
import connections
import userinfo
import uuid
import playing


def print_menu():
    print("1. Login")
    print("2. Register")
    print("3. Exit")

def login_menu():
    print("="*50)
    username = input("Enter username: ")
    password = input("Enter password: ")
    choice = int(input("Enter 1 for user, 2 for admin: "))
    if choice == 2:
        key = input("Enter the shared key: ")
    else:
        key = None

    account, admin, msg = login.login(connections.Cassandra_session, username, password, key)
    
    if account is None:
        print(msg)
        return None
    
    if admin:
        admin_menu()
    else:
        user_menu(connections.Mongo_client, account)


def admin_menu():
    print("="*50)
    print("Welcome, admin!")
    while True:
        print("1. View logs by user")
        print("2. View logs by game")
        print("3. Exit")
        choice = input("Enter option: ")
        
        if choice == "1":
            get_logs_by_user(connections.Cassandra_session)
        
        elif choice == "2":
            get_logs_by_game(connections.Cassandra_session)
            
        
        elif choice == "3":
            break

def user_menu(session_mongo, account):
    print("=" * 50)
    print(f"Welcome {account.username}!")

    # Asegurarse de que el identificador del usuario esté presente
    account_id = getattr(account, "account_id", None)

    if not account_id:
        print("Error: No se encontró el identificador del usuario.")
        return

    # Llamar a la función get_most_played_stats
    while True:
        mpg, mpc = userinfo.get_most_played_stats(session_mongo, account_id)
        
        option = choose_games_option()
        if option == 1:
            print("Keep playing")
            games = userinfo.get_most_played_games(connections.Dgraph_client, mpg)
            userinfo.format_games(games)

        elif option == 2:
            print("Recomendations")
            games = userinfo.cat(connections.Dgraph_client, mpc)
            userinfo.format_games(games)
        elif option == 3:
            break
        else:
            continue

        choice = int(input("Elige el juego con el numero o 0 para salir de tu sesion: "))
        if choice == 0:
            break
        game = games[choice-1]
        playing.playing(session_mongo, account_id, game["uid"], game["category"]["c_name"])

def choose_games_option():
    print("="*50)
    print("1. Keep playing")
    print("2. Recomendation")
    print("3. Exit")
    choice = input("Enter option: ")
    print("="*50)
    return int(choice)


def register_menu():
    print("="*50)
    print("Register as a user or admin")
    username = input("Enter username: ")
    password = input("Enter password: ")
    choice = int(input("Enter 1 for user, 2 for admin: "))
    if choice == 1:
        result, msg = register.register_user(connections.Cassandra_session, connections.Mongo_client,username, password)
        print(msg)
        if result is None:
            print(msg)
            return
        
        result, admin, msg = login.login(connections.Cassandra_session, username, password, "shared_key")
        print(msg)
        if result is None: 
            return 

        user_menu(connections.Mongo_client, result)

    elif choice == 2:
        charge = input("Enter charge: ")
        result, msg = register.register_admin(connections.Cassandra_session, username, password, charge)
        print(msg)
        if result is None:
            print(msg)
            return
        
        result, admin, msg = login.login(connections.Cassandra_session, username, password, "shared_key")
        print(msg)
        if result is None: 
            return 

        admin_menu()
        
def main():
    while True:
        print_menu()
        print("="*50)
        choice = input("Enter choice: ")
        if choice == "1":
            login_menu()
        elif choice == "2":
            register_menu()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()  
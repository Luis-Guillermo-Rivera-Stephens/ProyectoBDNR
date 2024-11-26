import login 
import register 
import connections
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
    print("ACCOUNT: ",account)
    if account is None:
        print(msg)
        return None
    
    if admin:
        admin_menu()
    else:
        user_menu(account)


def admin_menu():
    print("="*50)
    print("Welcome, admin!")
    while True:
        print("admin options")
        input("enter option")

def user_menu(account):
    print("="*50)
    print(f"Welcome {account.username}!")
    while True:
        print("user options")
        input("enter option")

def register_menu():
    print("="*50)
    print("Register as a user or admin")
    username = input("Enter username: ")
    password = input("Enter password: ")
    choice = int(input("Enter 1 for user, 2 for admin: "))
    if choice == 1:
        result, msg = register.register_user(connections.Cassandra_session, username, password)
        print(msg)
        if result is None:
            print(msg)
            return
        
        result, admin, msg = login.login(connections.Cassandra_session, username, password, "shared_key")
        print(msg)
        if result is None: 
            return 

        user_menu(result)

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
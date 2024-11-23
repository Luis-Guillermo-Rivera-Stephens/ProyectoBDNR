import uuid
import datetime
#import connections
#from queries import cassandra_queries
import json

def read_data_from_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)



def main():
    file_path = "./cassandra_data.json"
    data = read_data_from_json(file_path)

    administrators = data["administrators"]
    users = data["users"]
    logs = data["logs"]

    print(administrators)
    print(users)
    print(logs)

if __name__ == "__main__":
    main()

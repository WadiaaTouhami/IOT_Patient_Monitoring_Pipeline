from pymongo import MongoClient
from datetime import datetime
from pymongo.errors import ServerSelectionTimeoutError


def get_normal_logs(client):
    db = client["patient_monitoring"]
    collection = db["normal_logs"]
    logs = list(collection.find())
    print("\nNormal Logs:")
    for log in logs:
        print(log)
    return logs


def get_emergency_logs(client):
    db = client["patient_monitoring"]
    collection = db["emergency_logs"]
    logs = list(collection.find())
    print("\nEmergency Logs:")
    for log in logs:
        print(log)
    return logs


try:
    client = MongoClient(
        host="localhost",
        port=27017,
        username="root",
        password="root",
        authSource="admin",
    )
    client.server_info()
    print("Connected to MongoDB")

    normal_logs = get_normal_logs(client)
    emergency_logs = get_emergency_logs(client)

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if "client" in locals():
        client.close()

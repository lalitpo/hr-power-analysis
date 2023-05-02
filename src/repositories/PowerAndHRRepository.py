from src.config.LoadProperties import *
import pymongo


def store_athlete_info(record, db):
    pass


def store_athlete_activity(record, athletic_data_coll):
    athletic_data_coll.insert_one(record)
    pass


def store_records(record):
    hr_power_db = connect_database(configs.get("hr-power-db-url").data)
    store_athlete_info(record, hr_power_db)
    athletic_data = hr_power_db["Athletic-Data"]
    store_athlete_activity(record, athletic_data)


def connect_database(db_uri):
    # Create a new client and connect to the server
    client = pymongo.MongoClient(db_uri)
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("You are successfully connected to your Database!")
        return client["hrr-power-db"]
    except Exception as e:
        print(e)

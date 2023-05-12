import pymongo


def store_athlete_info(record, athlete_info_coll):
    athlete_info_coll.insert_one(record)
    pass


def store_athlete_activity(record, activity_data_coll):
    activity_data_coll.insert_one(record)
    pass


def store_records(record, db_conn):
    athlete_info = db_conn["Athlete-Info"]
    store_athlete_info(record, athlete_info)
    activity_data = db_conn["Activity-Data"]
    store_athlete_activity(record, activity_data)


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

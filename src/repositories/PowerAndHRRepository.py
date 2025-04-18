from datetime import datetime

import psycopg2
from colorama import Fore
from psycopg2 import extensions, OperationalError
from psycopg2._psycopg import IntegrityError
from sqlalchemy import create_engine

from src.config.LoadProperties import configs

"""
Saves a record in the specified table.

Parameters:
    data (dict): A dictionary containing the data to be saved.
    table (str): The name of the table where the record should be saved.

Returns:
    None

Raises:
    Exception: If an error occurs while storing the data in PostgresSQL.
"""


def save_record(data, table):
    keys = data.keys()
    values = data.values()
    columns = ', '.join(keys)
    value_placeholders = ', '.join(['%s'] * len(keys))
    insert_sql = f'INSERT INTO public."{table}" ({columns}) VALUES ({value_placeholders})'
    try:
        if table == "athlete-info":
            print(Fore.GREEN + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") +
                  " Saving athlete info of " + data["athlete_name"] + ", athlete id : " + data[
                      "athlete_id"] + " in Database.")
        else:
            print(Fore.GREEN + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") +
                  " Saving data of activity id : " + data["activity_id"] + " in Database.")
        hr_power_db_conn.cursor().execute(insert_sql, tuple(values))
        hr_power_db_conn.commit()
    except IntegrityError as e:
        print(Fore.RED + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") +
              " Error occurred while storing data in " + table + "in PostgresSQL:", str(e))
        if table == "athlete-info":
            print(Fore.LIGHTWHITE_EX + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") +
                  " Updating the table " + table + " by adding new activity IDs to the existing record of athlete ID: ")
            update_sql = f'UPDATE public."{table}" SET activities_ids = activities_ids || %s::bigint[] WHERE athlete_id = %s'
            hr_power_db_conn.cursor().execute(update_sql, (data['activities_ids'], data["athlete_id"]))
            hr_power_db_conn.commit()
            print(Fore.GREEN + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") +
                  " New activity IDs added to the existing record of athlete ID")
        else:
            print(Fore.LIGHTWHITE_EX + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") +
                  " The table is : " + table + ". So check why there is duplicate entry in database for it already.")
    except Exception as e:
        print(Fore.RED + (datetime.now()).strftime(
            "%Y-%m-%d %H:%M:%S") + " Error occurred while storing data in " + table + " in PostgresSQL:", str(e))


"""
Connects to a PostgreSQL database using the provided connection parameters.

Args:
    host (str): The hostname or IP address of the server.
    port (int): The port number on which the server is listening.
    database_name (str): The name of the database to connect to.
    user (str): The username for authentication.
    password (str): The password for authentication.

Returns:
    psycopg2.extensions.connection: The connection object if the connection is successful.

Raises:
    Exception: If the connection to the database fails.
"""


def connect_database(port, database_name, user, password):
    try:
        conn = psycopg2.connect(host="localhost",
                                port=port,
                                database=database_name,
                                user=user,
                                password=password)
        print(Fore.GREEN + (datetime.now()).strftime(
            "%Y-%m-%d %H:%M:%S") + " You are successfully connected to " + database_name + " database!")
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except Exception as e:
        print(Fore.RED + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Database could not be connected : ", e)


db_port = configs.get("db-port").data
db_name = configs.get("db-name").data
db_user = configs.get("db-user").data
db_password = configs.get("db-pass").data

hr_power_db_conn = connect_database(db_port, db_name, db_user, db_password)

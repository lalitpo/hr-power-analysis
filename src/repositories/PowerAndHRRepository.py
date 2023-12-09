import pandas as pd
import psycopg2
from psycopg2 import extensions, OperationalError
from sqlalchemy import create_engine

from src.config.LoadProperties import *


def save_profile_data(strava_data, table):
    keys = strava_data.keys()
    values = strava_data.values()
    columns = ', '.join(keys)
    value_placeholders = ', '.join(['%s'] * len(keys))
    sql = f'INSERT INTO public."{table}" ({columns}) VALUES ({value_placeholders})'
    try:
        hr_power_db_conn.cursor().execute(sql, tuple(values))
        hr_power_db_conn.commit()
    except Exception as e:
        # Handle the error
        print(Fore.RED + "Error occurred while storing data in PostgresSQL:", str(e))


def save_activity_data(strava_data, table):
    for data in strava_data:
        keys = data.keys()
        values = data.values()
        columns = ', '.join(keys)
        value_placeholders = ', '.join(['%s'] * len(keys))
        sql = f'INSERT INTO public."{table}" ({columns}) VALUES ({value_placeholders})'
        try:
            hr_power_db_conn.cursor().execute(sql, tuple(values))
            hr_power_db_conn.commit()
        except Exception as e:
            # Handle the error
            print(Fore.RED + "Error occurred while storing data in PostgreSQL:", str(e))


def create_schema(conn):
    for sql_query in sql_queries_list:
        try:
            conn.cursor().execute(sql_query)
            conn.commit()
        except OperationalError as msg:
            print(Fore.RED + "DB Schema creation failed: ", msg)
    print(Fore.GREEN + "DB Schema created successfully")


def connect_database(host, port, database_name, user, password):
    try:
        # Create a new client and connect to the server
        conn = psycopg2.connect(host=host,
                                port=port,
                                database=database_name,
                                user=user,
                                password=password)
        print(Fore.GREEN + "You are successfully connected to " + database_name + " database!")
        conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        create_schema(conn)
        return conn
    except Exception as e:
        print(Fore.RED + "Database could not be connected : ", e)


db_host = configs.get("db-host").data
db_port = configs.get("db-port").data
db_name = configs.get("db-name").data
db_user = configs.get("db-user").data
db_password = configs.get("db-pass").data

hr_power_db_conn = connect_database(db_host, db_port, db_name, db_user, db_password)

# Create a SQL engine using your database connection details
sql_engine = create_engine('postgresql://' + db_user + ':' + db_password + '@localhost:5432/' + db_name)


def get_athletic_data():
    return pd.read_sql(configs.get("athletic-record-query").data, sql_engine)

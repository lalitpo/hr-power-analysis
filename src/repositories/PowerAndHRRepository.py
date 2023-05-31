import psycopg2
import pandas as pd
from src.config.LoadProperties import *


def create_table(table1, table2):
    hr_power_db_conn.cursor().execute(table1)
    hr_power_db_conn.cursor().execute(table2)
    hr_power_db_conn.commit()


def get_athletic_data():
    return pd.read_sql(configs.get("athletic-record-query").data, hr_power_db_conn)


def save_data(strava_data, table):
    keys = strava_data.keys()
    values = strava_data.values()
    columns = ', '.join(keys)
    value_placeholders = ', '.join(['%s'] * len(keys))
    sql = f'INSERT INTO public."{table}" ({columns}) VALUES ({value_placeholders})'
    try:
        hr_power_db_conn.cursor().execute(sql, tuple(values))
        hr_power_db_conn.commit()
    except (psycopg2.Error, Exception) as e:
        # Handle the error
        print("Error occurred while storing data in PostgresSQL:", str(e))


def connect_database(db_name, db_user, db_password):
    try:
        # Create a new client and connect to the server
        conn = psycopg2.connect(host="localhost",
                                port="5432",
                                database=db_name,
                                user=db_user,
                                password=db_password)
        print("You are successfully connected to your Database!")
        return conn
    except Exception as e:
        print(e)


hr_power_db_conn = connect_database(configs.get("db-name").data, configs.get("db-user").data,
                                    configs.get("db-pass").data)

create_table(configs.get("athlete-info-table-query").data,
             configs.get("athletic-data-table-query").data)

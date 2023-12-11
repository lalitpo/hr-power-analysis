import datetime
import os

from colorama import Fore
from jproperties import Properties

configs = Properties()

with open('../resources/strava-config.properties', 'rb') as strava_config:
    configs.load(strava_config)
    print(Fore.GREEN + "Strava properties loaded.")

with open('../resources/db-config.properties', 'rb') as db_config:
    configs.load(db_config)
    print(Fore.GREEN + "Database connection properties loaded.")

with open('../resources/application-config.properties', 'rb') as app_config:
    configs.load(app_config)
    print(Fore.GREEN + "Application properties loaded.")

with open('../resources/DBSchemaQueries.sql', 'r') as db_schema_file:
    sql_queries_list = list(filter(None, db_schema_file.read().split(';')))

strava_url = configs.get("strava-url").data
imp_params = configs.get("params").data.split(",")

# Create a common folder "Strava Data"
data_folder = "Strava Data"
if not os.path.exists("../" + data_folder):
    os.makedirs("../" + data_folder)

def set_data_period():
    data_collection_period = int(configs.get("data-collection-period-in-weeks").data)
    my_date = datetime.date.today()
    year, week_num, _ = my_date.isocalendar()
    interval_list = []
    while data_collection_period > 0:
        interval_list.append(str(year) + (str(week_num) if week_num > 9 else "0" + str(week_num)))
        if week_num == 1:
            year = year - 1
            week_num = 52
        else:
            week_num = week_num - 1
        data_collection_period = data_collection_period - 1
    return interval_list


def get_data_url():
    base_url = strava_url + "/activities/activity_id/streams?stream_types%5B%5D="
    stream_types = configs.get("stream_types").data.split(",")
    return base_url + "&stream_types%5B%5D=".join(stream_types)


data_url_suffix = get_data_url()

data_period_list = set_data_period()

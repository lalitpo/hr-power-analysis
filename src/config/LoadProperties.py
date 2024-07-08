import os
from datetime import datetime as dt
from colorama import Fore
from jproperties import Properties

configs = Properties()

script_dir = os.path.dirname(__file__)


def get_config_path(config_file):
    return os.path.join(script_dir, '../../resources', config_file)


with open(get_config_path('strava-config.properties'), 'rb') as strava_config:
    configs.load(strava_config)
    print(Fore.GREEN + (dt.now()).strftime("%Y-%m-%d %H:%M:%S") + " Strava properties loaded.")

with open(get_config_path('db-config.properties'), 'rb') as db_config:
    configs.load(db_config)
    print(Fore.GREEN + (dt.now()).strftime("%Y-%m-%d %H:%M:%S") + " Database properties loaded.")

with open(get_config_path('application-config.properties'), 'rb') as app_config:
    configs.load(app_config)
    print(Fore.GREEN + (dt.now()).strftime("%Y-%m-%d %H:%M:%S") + " Application properties loaded.")

with open(get_config_path('RecordFetch.sql'), 'r') as db_file:
    retrieve_data_sql = db_file.read()

strava_url = configs.get("strava-url").data
imp_params = configs.get("params").data.split(",")

data_folder = "Strava Data"
remove_columns = configs.get("ignore-columns").data


def get_weeks(weeks, year):
    week_year = [f"{year}{week}" for week in weeks]
    return week_year


data_period_list = get_weeks(configs.get("data-collection-week").data.split(","),
                             configs.get("data-collection-year").data)


def get_data_url():
    base_url = strava_url + "/activities/activity_id/streams?stream_types%5B%5D="
    stream_types = configs.get("stream_types").data.split(",")
    return base_url + "&stream_types%5B%5D=".join(stream_types)


data_url_suffix = get_data_url()

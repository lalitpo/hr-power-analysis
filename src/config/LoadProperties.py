from datetime import datetime as dt

from colorama import Fore
from jproperties import Properties

configs = Properties()

with open('/Users/lalit/Desktop/self/Uni/MS Project '
          'Thesis/codebase/hr-power-reln-app/resources/strava-config.properties', 'rb') as strava_config:
    configs.load(strava_config)
    print(Fore.GREEN + (dt.now()).strftime("%Y-%m-%d %H:%M:%S") + " Strava properties loaded.")

with open('/Users/lalit/Desktop/self/Uni/MS Project Thesis/codebase/hr-power-reln-app/resources/db-config.properties',
          'rb') as db_config:
    configs.load(db_config)
    print(Fore.GREEN + (dt.now()).strftime("%Y-%m-%d %H:%M:%S") + " Database connection properties loaded.")

with open('/Users/lalit/Desktop/self/Uni/MS Project '
          'Thesis/codebase/hr-power-reln-app/resources/application-config.properties', 'rb') as app_config:
    configs.load(app_config)
    print(Fore.GREEN + (dt.now()).strftime("%Y-%m-%d %H:%M:%S") + " Application properties loaded.")

with open('/Users/lalit/Desktop/self/Uni/MS Project Thesis/codebase/hr-power-reln-app/resources/DBSchemaQueries.sql',
          'r') as db_schema_file:
    sql_queries_list = list(filter(None, db_schema_file.read().split(';')))

with open('/Users/lalit/Desktop/self/Uni/MS Project Thesis/codebase/hr-power-reln-app/resources/RecordFetch.sql',
          'r') as db_file:
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

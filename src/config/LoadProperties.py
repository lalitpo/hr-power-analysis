import datetime

from jproperties import Properties

configs = Properties()

with open('../resources/strava-config.properties', 'rb') as strava_config:
    configs.load(strava_config)
    print("Strava properties loaded.")

with open('../resources/db-config.properties', 'rb') as db_config:
    configs.load(db_config)
    print("Database connection properties loaded.")


with open('../resources/application-config.properties', 'rb') as app_config:
    configs.load(app_config)
    print("Application properties loaded.")

with open('../resources/DBSchemaQueries.sql', 'r') as db_schema_file:
    sql_queries_list = db_schema_file.read().split(';')

minimum_activity_length = int(configs.get("min-activity-length-in-sec").data)
strava_url = configs.get("strava-url").data

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

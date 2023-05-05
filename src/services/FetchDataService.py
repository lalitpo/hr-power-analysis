from src.services.LoginStravaService import *
from src.repositories.PowerAndHRRepository import *
import urllib.parse
import json
import time

athlete_ids = open('../../resources/pro-athlete-id.txt').readlines()
data_collection_period = configs.get("data-collection-period-in-weeks").data


def get_activity_url():
    base_url = configs.get("strava-url").data + "/activities/activity_id/streams?stream_types%5B%5D="
    stream_types = configs.get("stream_types").data.split(",")
    return base_url + "&stream_types%5B%5D=".join(stream_types)


def get_activity_ids():
    base_url = configs.get("strava-url").data + "/pros/athlete_id/interval?"
    interval_param = configs.get("activity-interval").data.split(",")
    interval_data = {"202318", "week", "miles", "0"}
    query_param_string = dict(zip(interval_param, interval_data))
    activity_url = base_url + urllib.parse.urlencode(query_param_string)
    return activity_url


act_data_url = get_activity_url()
ath_act_url = get_activity_ids()
hr_power_db = connect_database(configs.get("hr-power-db-url").data)


def store_activities_data(activities_list):
    for activity in activities_list:
        time.sleep(5)  # latency so that strava doesn't block us for scraping using a bot.
        driver.get(act_data_url.replace("activity_id", activity))
        pre = driver.find_element(By.TAG_NAME, "pre").text
        data = json.loads(pre)
        activity_info = {"activity_id": activity.strip()}
        data.update(activity_info)
        store_records(data, hr_power_db)


for athlete in athlete_ids:
    url2 = ath_act_url.replace("athlete_id", athlete)
    driver.get(url2)
    pre = driver.find_element(By.TAG_NAME, "pre").text
    store_activities_data(ath_act_url)

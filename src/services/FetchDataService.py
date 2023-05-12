import datetime
import json
import time
import urllib.parse
from bs4 import BeautifulSoup
from src.repositories.PowerAndHRRepository import *
from src.services.LoginStravaService import *

athlete_ids = open('../../resources/pro-athlete-id.txt').readlines()
hr_power_db = connect_database(configs.get("hr-power-db-url").data)


def create_activity_url():
    base_url = configs.get("strava-url").data + "/activities/activity_id/streams?stream_types%5B%5D="
    stream_types = configs.get("stream_types").data.split(",")
    return base_url + "&stream_types%5B%5D=".join(stream_types)


def create_interval_list():
    data_collection_period = int(configs.get("data-collection-period-in-weeks").data)
    my_date = datetime.date.today()
    year, week_num, day_of_week = my_date.isocalendar()
    interval_list = []
    while data_collection_period > 0:
        interval_list.append(str(year) + str(week_num))
        if week_num == 1:
            year = year - 1
            week_num = 52
        else:
            week_num = week_num - 1
        data_collection_period = data_collection_period - 1
    return interval_list


def get_weekly_urls(intervals_list):
    base_url = configs.get("strava-url").data + "/pros/athlete_id#interval?"
    interval_param = configs.get("activity-interval").data.split(",")
    activity_url_list = []
    for k in intervals:
        interval_info = [k, "week", "miles", "0"]
        query_param_string = dict(zip(interval_param, interval_info))
        activity_url = base_url + urllib.parse.urlencode(query_param_string)
        activity_url_list.append(activity_url)
    return activity_url_list


base_act_data_url = create_activity_url()

intervals = create_interval_list()


def get_activity_ids(athlete_id):
    weekly_urls = get_weekly_urls(intervals)

    activity_ids_list = []
    for week_url in weekly_urls:
        week_url = week_url.replace("athlete_id", athlete_id)
        driver.get(week_url)
        time.sleep(10)  # latency so that strava doesn't block us for scraping using a bot.
        div_element = driver.find_element(By.CSS_SELECTOR, "div.content.react-feed-component").get_attribute(
            "outerHTML")
        # parse the HTML using BeautifulSoup
        attribute_list = BeautifulSoup(div_element, 'html.parser').contents[0].__getattribute__("attrs")
        activity_list = json.loads(attribute_list["data-react-props"])['appContext']['preFetchedEntries']
        for activity in activity_list:
            if activity['entity'] == "GroupActivity":
                activity_ids_list.append(str(activity['rowData']['activities'][0]['entity_id']))
            elif activity['entity'] == "Activity":
                activity_ids_list.append(activity['activity']['id'])
    return activity_ids_list


def store_activities_data(athlete_details, activities_list):
    for activity in activities_list:
        time.sleep(5)  # latency so that strava doesn't block us for scraping using a bot.
        driver.get(base_act_data_url.replace("activity_id", activity))
        pre = driver.find_element(By.TAG_NAME, "pre").text
        activity_data = json.loads(pre)
        activities_stored = []
        if len(activity_data['watts']) > 7200:
            activity_info = {"activity_id": activity.strip()}
            activity_data.update(activity_info)
            activity_data_conn = hr_power_db["Activity-Data"]
            store_athlete_activity(activity_data, activity_data_conn)
            activities_stored.append(activity)
        athlete_data = {"athlete_name": athlete_details['athlete_name'], "athlete_id": athlete_details['athlete_id'],
                        "location": athlete_details['location'], "activities_ids": activities_stored}
        athlete_info_conn = hr_power_db["Athlete-Info"]
        store_athlete_info(athlete_data, athlete_info_conn)


def get_athlete_info(athlete_id):
    athlete_url = configs.get("strava-url").data + "/pros/" + athlete_id
    driver.get(athlete_url)
    athlete_name = driver.find_element(By.CSS_SELECTOR, "h1.text-title1.athlete-name").text
    athlete_location = driver.find_element(By.CSS_SELECTOR, "div.location").text
    athlete_details = {"athlete_name": athlete_name,
                       "athlete_id": athlete_id,
                       "location": athlete_location}
    return athlete_details


for athlete in athlete_ids:
    athlete_info = get_athlete_info(athlete.strip())
    activities_ids_list = get_activity_ids(athlete.strip())
    store_activities_data(athlete_info, activities_ids_list)
    print("Data stored for athlete :" + athlete_info['athlete_name'])
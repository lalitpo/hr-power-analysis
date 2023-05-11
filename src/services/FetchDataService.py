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


intervals = create_interval_list()


def get_activity_ids(athlete_id):
    weekly_urls = get_weekly_urls(intervals)
    string_start = "www.strava.com%2Factivities%2F"
    string_end = "%3F"

    activity_ids_list = []
    for week_url in weekly_urls:
        week_url = week_url.replace("athlete_id", athlete_id)
        driver.get(week_url)
        div_element = driver.find_element(By.CSS_SELECTOR, "div.content.react-feed-component").get_attribute("outerHTML")
        # parse the HTML using BeautifulSoup
        attribute_list = BeautifulSoup(div_element, 'html.parser').contents[0].__getattribute__("attrs")
        activity_list = json.loads(attribute_list["data-react-props"])['appContext']['preFetchedEntries']
        for activity in activity_list:
            activity_id = activity['rowData']['activities'][0]['entity_id']
            activity_ids_list.extend(activity_id)
        #cur_week_activities = re.findall(f'{string_start}(.*?){string_end}', div_element)
        #
        print("abc")
    return activity_ids_list


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
    act_data_url = create_activity_url()
    activities_ids_list = get_activity_ids(athlete.strip())
    store_activities_data(activities_ids_list)

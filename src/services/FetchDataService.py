import datetime
import json
import re
import time
import urllib.parse
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from src.constants.PowerAndHRConstants import *
from src.repositories.PowerAndHRRepository import *
from src.services.LoginStravaService import *
from _datetime import datetime as dt

athlete_ids = open('../../resources/pro-athlete-id.txt').readlines()


def create_activity_url():
    base_url = strava_url + "/activities/activity_id/streams?stream_types%5B%5D="
    stream_types = configs.get("stream_types").data.split(",")
    return base_url + "&stream_types%5B%5D=".join(stream_types)


base_act_data_url = create_activity_url()
minimum_activity_length = int(configs.get("min-activity-length-in-sec").data)


def create_interval_list():
    data_collection_period = int(configs.get("data-collection-period-in-weeks").data)
    my_date = datetime.date.today()
    year, week_num, day_of_week = my_date.isocalendar()
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


intervals = create_interval_list()


def get_weekly_urls():
    base_url = strava_url + "/pros/athlete_id#interval?"
    interval_param = configs.get("activity-interval").data.split(",")
    activity_url_list = []
    for k in intervals:
        interval_info = [k, "week", "miles", "0"]
        query_param_string = dict(zip(interval_param, interval_info))
        activity_url = base_url + urllib.parse.urlencode(query_param_string)
        activity_url_list.append(activity_url)
    return activity_url_list


def get_activity_ids(ath_id):
    weekly_urls = get_weekly_urls()

    activity_ids_list = []
    for week_url in weekly_urls:
        week_url = week_url.replace(athlete_id, ath_id)
        driver.get(week_url)
        time.sleep(5)
        div_element = driver.find_element(By.CSS_SELECTOR, "div.content.react-feed-component").get_attribute(
            "outerHTML")
        # parse the HTML using BeautifulSoup
        attribute_list = BeautifulSoup(div_element, 'html.parser').contents[0].__getattribute__("attrs")
        activity_list = json.loads(attribute_list["data-react-props"])['appContext']['preFetchedEntries']

        for act in activity_list:
            if act[entity] == "GroupActivity" and act[rowData][activities][0][activity_type] == ride:
                activity_ids_list.append(str(act[rowData][activities][0][entity + '_' + id]))
            elif act[entity] == "Activity" and act[activity][activity_type] == ride:
                activity_ids_list.append(act[activity][id])
    return list(set(activity_ids_list))


def save_activity_data(activities_list):
    activities_stored = []
    for act in activities_list:
        time.sleep(5)  # latency so that strava doesn't block us for scraping using a bot.
        driver.get(strava_url + "/activities/" + act)
        activity_summary = driver.find_element(By.CSS_SELECTOR, "div.details").get_attribute(
            "outerHTML")
        meta_data = BeautifulSoup(activity_summary, 'html.parser').text
        activity_meta_data = re.split(r'\n+', meta_data)
        main_stats_div = driver.find_element(By.CSS_SELECTOR, "div.spans8.activity-stats.mt-md.mb-md").get_attribute(
            "outerHTML")
        main_stats_list = BeautifulSoup(main_stats_div, 'html.parser').contents[0].__getattribute__("contents")
        head_data = re.split(r'\n+', main_stats_list[1].text)
        time.sleep(5)  # latency so that strava doesn't block us for scraping using a bot.
        driver.get(base_act_data_url.replace(activity + '_' + id, act))
        pre = driver.find_element(By.TAG_NAME, "pre").text
        activity_info = json.loads(pre)
        activity_duration_split = head_data[3].split(':')
        if len(activity_duration_split) == 2:
            activity_duration = datetime.timedelta(minutes=int(activity_duration_split[0]),
                                                   seconds=int(activity_duration_split[1]))
        else:
            activity_duration = datetime.timedelta(hours=int(activity_duration_split[0]),
                                                   minutes=int(activity_duration_split[1]),
                                                   seconds=int(activity_duration_split[2]))
        if watts in activity_info:
            activity_data = {activity + '_' + id: act.strip(),
                             "activity_date": dt.strptime(activity_meta_data[1].split(', ')[1], '%d %B %Y').date(),
                             "activity_distance": head_data[1].split(' ')[0],
                             "activity_duration": str(activity_duration),
                             "elevation": head_data[5].replace(',', '').split(' ')[0]}
            activity_data.update(activity_info)
            save_data(activity_data, "athletic-data")
            activities_stored.append(act)
    return activities_stored


def store_activities_data(athlete_details, activities_list):
    # create the athletic data table with constraints.
    hr_power_db_conn.cursor().execute(configs.get("athletic-data-table-query").data)
    # save the athletic data into the athletic-data table created.
    activities_saved = save_activity_data(activities_list)
    athlete_data = {athlete_name: athlete_details[athlete_name], athlete_id: athlete_details[athlete_id],
                    location: athlete_details[location], "activities_ids": [int(x) for x in activities_saved]}
    save_data(athlete_data, "athlete-info")


def get_athlete_info(athl_id):
    athlete_url = strava_url + "/pros/" + athl_id
    driver.get(athlete_url)
    ath_name = driver.find_element(By.CSS_SELECTOR, "h1.text-title1.athlete-name").text
    try:
        athlete_location = driver.find_element(By.CSS_SELECTOR, "div.location")
    # Perform actions with the found element
    except NoSuchElementException:
        athlete_location = "NA"

    athlete_details = {"athlete_name": ath_name,
                       "athlete_id": athl_id,
                       "location": athlete_location.text}
    print(athlete_details)
    return athlete_details


for athlete in athlete_ids:
    athlete_info = get_athlete_info(athlete.strip())
    activities_ids_list = get_activity_ids(athlete.strip())
    print(activities_ids_list)
    store_activities_data(athlete_info, activities_ids_list)
    print("Data stored for athlete :" + athlete_info[athlete_name])

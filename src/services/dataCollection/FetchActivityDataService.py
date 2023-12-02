import urllib.parse
import datetime
import json
import time
import re

from _datetime import datetime as dt

from colorama import Fore

from src.constants.PowerAndHRConstants import watts

from src.config.LoadProperties import data_url_suffix
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from src.config.LoadProperties import configs, data_period_list, strava_url
from src.services.dataCollection.LoginStravaService import browser_driver
from src.constants.PowerAndHRConstants import (athlete_id, entity, rowData, activities,
                                               activity_type, ride, activity, html_parser)


def get_weekly_urls():
    base_url = strava_url + "/pros/athlete_id#interval?"
    interval_param = configs.get("activity-interval").data.split(",")
    activity_url_list = []
    for k in data_period_list:
        interval_info = [k, "week", "miles", "0"]
        query_param_string = dict(zip(interval_param, interval_info))
        activity_url = base_url + urllib.parse.urlencode(query_param_string)
        activity_url_list.append(activity_url)
    return activity_url_list


def get_activity_ids(ath_id):
    weekly_urls = get_weekly_urls()
    try:
        activity_ids_list = []
        for week_url in weekly_urls:
            week_url = week_url.replace(athlete_id, ath_id)
            browser_driver.get(week_url)
            time.sleep(5)
            div_element = browser_driver.find_element(By.CSS_SELECTOR,
                                                      "div.content.react-feed-component").get_attribute(
                "outerHTML")
            # parse the HTML using BeautifulSoup
            attribute_list = BeautifulSoup(div_element, html_parser).contents[0].__getattribute__("attrs")
            activity_list = json.loads(attribute_list["data-react-props"])['appContext']['preFetchedEntries']

            for act in activity_list:
                if act[entity] == "GroupActivity" and act[rowData][activities][0][activity_type] == ride:
                    activity_ids_list.append(str(act[rowData][activities][0][entity + '_' + id]))
                elif act[entity] == "Activity" and act[activity][activity_type] == ride:
                    activity_ids_list.append(act[activity][id])
        return list(set(activity_ids_list))
    except Exception as e:
        print("Error occurred while getting activity ids:", str(e))


def get_athlete_info(athl_id):
    athlete_url = strava_url + "/pros/" + athl_id
    browser_driver.get(athlete_url)
    ath_name = browser_driver.find_element(By.CSS_SELECTOR, "h1.text-title1.athlete-name").text
    athlete_location = "NA"
    try:
        athlete_location = browser_driver.find_element(By.CSS_SELECTOR, "div.location").text
    except NoSuchElementException:
        print("Location not present for athlete :" + ath_name + "athlete_id" + athl_id)

    athlete_details = {"athlete_name": ath_name,
                       "athlete_id": athl_id,
                       "location": athlete_location}
    print(athlete_details)
    return athlete_details


def get_activity_data(activities_list):
    activity_data = []
    for act in activities_list:
        try:
            time.sleep(5)  # latency so that strava doesn't block us for scraping.
            browser_driver.get(strava_url + "/activities/" + act)
            activity_summary = browser_driver.find_element(By.CSS_SELECTOR, "div.details").get_attribute(
                "outerHTML")
            meta_data = BeautifulSoup(activity_summary, html_parser).text
            activity_meta_data = re.split(r'\n+', meta_data)
            main_stats_div = browser_driver.find_element(By.CSS_SELECTOR,
                                                         "div.spans8.activity-stats.mt-md.mb-md").get_attribute(
                "outerHTML")
            main_stats_list = BeautifulSoup(main_stats_div, html_parser).contents[0].__getattribute__("contents")
            head_data = re.split(r'\n+', main_stats_list[1].text)
            time.sleep(5)  # latency so that strava doesn't block us for scraping.
            browser_driver.get(data_url_suffix.replace(activity + '_' + id, act))
            pre = browser_driver.find_element(By.TAG_NAME, "pre").text
            activity_info = json.loads(pre)
            if 's' in head_data[3]:
                activity_duration = "00:00" + head_data[3][:-1]
            else:
                activity_duration_split = head_data[3].split(':')
                if len(activity_duration_split) == 2:
                    activity_duration = datetime.timedelta(minutes=int(activity_duration_split[0]),
                                                           seconds=int(activity_duration_split[1]))
                else:
                    activity_duration = datetime.timedelta(hours=int(activity_duration_split[0]),
                                                           minutes=int(activity_duration_split[1]),
                                                           seconds=int(activity_duration_split[2]))
            if watts in activity_info:
                elev = head_data[5].replace(',', '').split(' ')[0]
                activity_data = {activity + '_' + id: act.strip(),
                                 "activity_date": dt.strptime(activity_meta_data[1].split(', ')[1], '%d %B %Y').date(),
                                 "activity_distance": head_data[1].split(' ')[0],
                                 "activity_duration": str(activity_duration),
                                 "elevation": '0' if elev == '' else elev}
                activity_data.update(activity_info)
        except Exception as e:
            print(Fore.RED + "Error occurred while saving activity data:", str(e), act)
    return activity_data

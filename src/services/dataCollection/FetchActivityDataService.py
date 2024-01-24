import datetime
import json
import re
import time
import urllib.parse
from _datetime import datetime as dt
from datetime import datetime as dtt

from bs4 import BeautifulSoup
from colorama import Fore
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from src.config.LoadProperties import configs, data_period_list, strava_url
from src.config.LoadProperties import data_url_suffix, imp_params
from src.constants.PowerAndHRConstants import activity_id, power, average, maxx, speed, cadence, heart_rate
from src.constants.PowerAndHRConstants import (athlete_id, entity, rowData, activities,
                                               activity_type, ride, activity, html_parser)

athlete_type = configs.get("athlete-type").data

"""
Generate a list of weekly activity URLs.

Returns:
    activity_url_list (list): A list of URLs for weekly activities.
"""


def get_weekly_urls():
    base_url = strava_url + "/" + athlete_type.lower() + "/" + "athlete_id#interval?"
    interval_param = configs.get("activity-interval").data.split(",")
    activity_url_list = []
    for k in data_period_list:
        interval_info = [k, "week", "miles", "0"]
        query_param_string = dict(zip(interval_param, interval_info))
        activity_url = base_url + urllib.parse.urlencode(query_param_string)
        activity_url_list.append(activity_url)
    return activity_url_list


"""
    Retrieves a list of activity IDs associated with a given athlete ID.

    Parameters:
        ath_id (int): The ID of the athlete.

    Returns:
        list: A list of unique activity IDs.
"""


def get_activity_ids(browser_driver, ath_id, week_url):
    try:
        activity_ids_list = []
        url = week_url.replace(athlete_id, ath_id)
        print(Fore.LIGHTWHITE_EX + (dtt.now()).strftime("%Y-%m-%d %H:%M:%S") + " Collecting activity ids "
                                                                               "of: " + url)
        browser_driver.get(url)
        time.sleep(20)

        div_element = browser_driver.find_element(By.CSS_SELECTOR, "div.content.react-feed-component").get_attribute(
            "outerHTML")
        # parse the HTML using BeautifulSoup
        attribute_list = BeautifulSoup(div_element, html_parser).contents[0].__getattribute__("attrs")
        activity_list = json.loads(attribute_list["data-react-props"])['appContext']['preFetchedEntries']

        for act in activity_list:  # Convert minutes and seconds to seconds
            if act[entity] == "GroupActivity" and ride.lower() in act[rowData][activities][0][activity_type].lower():
                activity_ids_list.append(str(act[rowData][activities][0][entity + '_' + activity_id]))
            elif act[entity] == "Activity" and ride.lower() in act[activity][activity_type].lower():
                activity_ids_list.append(act[activity][activity_id])
        return list(set(activity_ids_list))
    except Exception as e:
        print(Fore.RED + (dtt.now()).strftime("%Y-%m-%d %H:%M:%S") + " Error occurred while getting activity "
                                                                     "ids:", str(e))


"""
    Retrieves information about an athlete based on their athlete ID.

    Args:
        athl_id (int): The ID of the athlete.

    Returns:
        dict: A dictionary containing the athlete's name, ID, and location information.

    Raises:
        NoSuchElementException: If the athlete's location is not found.
"""


def get_athlete_info(browser_driver, athl_id):
    athlete_url = strava_url + "/" + athlete_type.lower() + "/" + athl_id
    browser_driver.get(athlete_url)
    ath_name = browser_driver.find_element(By.CSS_SELECTOR, "h1.text-title1.athlete-name").text
    athlete_location = "NA"
    try:
        athlete_location = browser_driver.find_element(By.CSS_SELECTOR, "div.location").text
    except NoSuchElementException:
        print(Fore.RED + (dtt.now()).strftime(
            "%Y-%m-%d %H:%M:%S") + " Location not present for athlete : " + ath_name + ", and athlete_id : " + athl_id)

    athlete_details = {"athlete_name": ath_name,
                       "athlete_id": athl_id,
                       "location": athlete_location}
    print(Fore.LIGHTWHITE_EX + (dtt.now()).strftime("%Y-%m-%d %H:%M:%S") + " Athlete details : ", athlete_details)
    return athlete_details


"""
    Checks if the specified parameters exist in the given activity information.

    Parameters:
        activity_info (dict): A dictionary containing information about an activity.

    Returns:
        bool: True if both parameters exist and have non-zero length values, False otherwise.
"""


def param_exists(activity_info):
    return (
            imp_params[0] in activity_info
            and len(activity_info[imp_params[0]]) != 0
            and imp_params[1] in activity_info
            and len(activity_info[imp_params[1]]) != 0
    )


"""
    Calculate the duration of an activity based on the provided head data.

    Parameters:
        head_data (list): A list containing information about the activity. The 
                          third element of the list represents the duration of 
                          the activity.

    Returns:
        datetime.timedelta: The duration of the activity as a timedelta object.
"""


def calc_activity_duration(head_data):
    if 's' in head_data[3]:
        duration = "00:00" + head_data[3][:-1]
    else:
        duration_split = head_data[3].split(':')
        if len(duration_split) == 2:
            duration = datetime.timedelta(minutes=int(duration_split[0]),
                                          seconds=int(duration_split[1]))
        else:
            duration = datetime.timedelta(hours=int(duration_split[0]),
                                          minutes=int(duration_split[1]),
                                          seconds=int(duration_split[2]))
    return duration


"""
    Retrieves data for each activity in the given activities list.
    
    Parameters:
        activities_list (list): A list of activity IDs.
    
    Returns:
        list: A list of activity data dictionaries.
"""


def get_data(sub_type, type, stats_data):
    if type == power:
        if stats_data[2] == 'Weighted Avg Power':
            return ''.join([c for c in stats_data[1] if c.isdigit()])
        pow_idx = stats_data.index(power) if power in stats_data else -1
        if pow_idx != -1 and stats_data[3] == sub_type:
            return ''.join([c for c in stats_data[pow_idx + 1] if c.isdigit()])
        if pow_idx != -1 and stats_data[4] == sub_type:
            return ''.join([c for c in stats_data[pow_idx + 2] if c.isdigit()])
        else:
            return '0'
    if type == speed:
        speed_idx = stats_data.index(speed) if speed in stats_data else -1
        if speed_idx != -1 and stats_data[3] == sub_type:
            return ''.join([c if c.isdigit() or c == '.' else '' for c in stats_data[speed_idx + 1]])
        if speed_idx != -1 and stats_data[4] == sub_type:
            return ''.join([c if c.isdigit() or c == '.' else '' for c in stats_data[speed_idx + 2]])
        else:
            return '0'
    if type == cadence:
        cadence_idx = stats_data.index(cadence) if cadence in stats_data else -1
        if cadence_idx != -1 and stats_data[3] == sub_type:
            return ''.join([c for c in stats_data[cadence_idx + 1] if c.isdigit()])
        if cadence_idx != -1 and stats_data[4] == sub_type:
            return ''.join([c for c in stats_data[cadence_idx + 2] if c.isdigit()])
        else:
            return '0'
    if type == heart_rate:
        hr_idx = stats_data.index(heart_rate) if heart_rate in stats_data else -1
        if hr_idx != -1 and stats_data[3] == sub_type:
            return ''.join([c for c in stats_data[hr_idx + 1] if c.isdigit()])
        if hr_idx != -1 and stats_data[4] == sub_type:
            return ''.join([c for c in stats_data[hr_idx + 2] if c.isdigit()])
        else:
            return '0'


def get_activities_data(browser_driver, activities_list):
    activities_data = []
    for act in activities_list:
        try:
            print(Fore.LIGHTWHITE_EX + (dtt.now()).strftime("%Y-%m-%d %H:%M:%S") +
                  " Fetching Data for activity ID : " + act)
            time.sleep(10)  # latency so that strava doesn't block us for scraping.
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
            secondary_stats_data = re.split(r'\n+', main_stats_list[3].text)
            more_stats_data = re.split(r'\n+', main_stats_list[5].text)
            time.sleep(10)  # latency so that strava doesn't block us for scraping.
            browser_driver.get(data_url_suffix.replace(activity + '_' + activity_id, act))
            pre = browser_driver.find_element(By.TAG_NAME, "pre").text
            activity_info = json.loads(pre)

            if param_exists(activity_info):
                activity_duration = calc_activity_duration(head_data)
                elev = head_data[5].replace(',', '').split(' ')[0]
                activity_info.update({activity + '_' + activity_id: act.strip(),
                                      "activity_date": dt.strptime(activity_meta_data[1].split(', ')[1],
                                                                   '%d %B %Y').date(),
                                      "activity_distance": head_data[1].split(' ')[0],
                                      "activity_duration": str(activity_duration),
                                      "elevation": '0' if elev == '' else elev,
                                      "average_power": get_data(average, power, more_stats_data),
                                      "max_power": get_data(maxx, power, more_stats_data),
                                      "weighted_average_power": get_data('Weighted', power, secondary_stats_data),
                                      "average_speed": get_data(average, speed, more_stats_data),
                                      "max_speed": get_data(maxx, speed, more_stats_data),
                                      "average_cadence": get_data(average, cadence, more_stats_data),
                                      "max_cadence": get_data(maxx, cadence, more_stats_data),
                                      "average_heart_rate": get_data(average, heart_rate, more_stats_data),
                                      "max_heart_rate": get_data(maxx, heart_rate, more_stats_data)
                                      })
                activities_data.append(activity_info)
            else:
                print(Fore.RED + (dtt.now()).strftime("%Y-%m-%d %H:%M:%S") + " No data fetched for activity "
                                                                             "ID : " + act +
                      ". It could be due to the activity was " +
                      "did not record either of heartrate " +
                      "or watts or both at all.")
        except Exception as e:
            print(Fore.RED + (dtt.now()).strftime("%Y-%m-%d %H:%M:%S") +
                  " Error occurred while fetching data for "
                  "activity : ", str(e), act)
    return activities_data

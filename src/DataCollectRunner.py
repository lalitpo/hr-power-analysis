import time
from datetime import datetime

from colorama import Fore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from src.config.LoadProperties import configs
from src.constants.PowerAndHRConstants import athlete_name
from src.services.dataCollection.FetchActivityDataService import get_athlete_info, get_activity_ids, \
    get_activities_data, get_weekly_urls
from src.services.dataCollection.LoginStravaService import login_strava, exit_strava
from src.services.dataCollection.StoreActivityDataService import save_athlete_data

athlete_id = configs.get("athlete-id").data


def fetch_week_data(week):
    # Chrome Headless Mode
    options = Options()
    # options.add_argument('--headless=new')

    """
    STEP 1 : Login into strava with user account configured in strava-config properties file.
    No need to download chromedriver,
    This installs driver everytime to avoid downloading manually every new patch or version of Chrome.
    """
    browser_driver = webdriver.Chrome(options, service=ChromeService(ChromeDriverManager().install()))

    login_strava(browser_driver)

    """
    # STEP 2 Pull Data for each athlete.
    # Retrieves athlete information and activity data based on the provided athlete ID.

    Args:
        ath_id (str): The ID of the athlete.

    Returns:
        tuple: A tuple containing the athlete information and activity data.
    """

    def pull_data(driver, ath_id, url):
        ath_bio = get_athlete_info(driver, ath_id.strip())
        act_ids_list = get_activity_ids(driver, ath_id.strip(), url)
        print(Fore.LIGHTWHITE_EX + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") +
              " Total number of activity IDs collected for athlete ID " + ath_bio["athlete_id"] + " : " +
              str(len(act_ids_list)))
        act_data = get_activities_data(driver, act_ids_list)
        return ath_bio, act_data

    """
    # STEP 3: Store Data of each athlete in the database.

    Store the athlete's biography and data in the database.

    Parameters:
        bio (str): The athlete's biography.
        data (dict): The athlete's data.

    Returns:
        None
    """

    def store_in_db(bio, data):
        save_athlete_data(bio, data)

    athlete_bio, activities_data = pull_data(browser_driver, athlete_id, week)
    store_in_db(athlete_bio, activities_data)
    print(Fore.GREEN + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Data stored for athlete : " +
          athlete_bio[
              athlete_name] + " with Athlete ID :" + athlete_id)
    print(Fore.GREEN + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Closing Chrome session of Strava.")

    exit_strava(browser_driver)


weekly_urls = get_weekly_urls()

for week_url in weekly_urls:
    fetch_week_data(week_url)
    time.sleep(240)

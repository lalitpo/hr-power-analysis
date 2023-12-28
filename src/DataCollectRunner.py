from datetime import datetime
from time import sleep

from colorama import Fore

from src.constants.PowerAndHRConstants import athlete_name
from src.services.dataCollection.FetchActivityDataService import get_athlete_info, get_activity_ids, \
    get_activities_data, get_weekly_urls
from src.services.dataCollection.LoginStravaService import login_strava
from src.services.dataCollection.StoreActivityDataService import save_athlete_data

athlete_ids = open('../resources/pro-athlete-id.txt').readlines()

weekly_urls = get_weekly_urls()
for week_url in weekly_urls:

    while datetime.now().minute not in {0, 15, 30, 45}:
        # Wait 1 second until we are synced up with the 'every 15 minutes' clock
        sleep(1)

        """
        # STEP 1 : Login into strava with user account configured in strava-config properties file.
        """
        login_strava()

        """
    # STEP 2 Pull Data for each athlete.
    Retrieves athlete information and activity data based on the provided athlete ID.

    Args:
        ath_id (str): The ID of the athlete.

    Returns:
        tuple: A tuple containing the athlete information and activity data.
    """


        def pull_data(ath_id):
            ath_bio = get_athlete_info(ath_id.strip())
            act_ids_list = get_activity_ids(ath_id.strip())
            print(Fore.LIGHTWHITE_EX + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") +
                  " Total number of activity IDs collected for athlete ID " + ath_bio["athlete_id"] + " : " +
                  str(len(act_ids_list)))
            print(act_ids_list)
            act_data = get_activities_data(act_ids_list)
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


        for athlete_id in athlete_ids:
            athlete_bio, activities_data = pull_data(athlete_id)
            store_in_db(athlete_bio, activities_data)
            print(Fore.GREEN + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Data stored for athlete : " +
                  athlete_bio[
                      athlete_name] + " with Athlete ID :" + athlete_id)

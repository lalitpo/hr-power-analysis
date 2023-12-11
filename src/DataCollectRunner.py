from colorama import Fore

from src.constants.PowerAndHRConstants import athlete_name
from src.services.dataCollection.FetchActivityDataService import get_athlete_info, get_activity_ids, get_activities_data
from src.services.dataCollection.LoginStravaService import login_strava
from src.services.dataCollection.StoreActivityDataService import save_athlete_data

athlete_ids = open('../resources/pro-athlete-id.txt').readlines()

"""
# STEP 1 : Login into strava with user account configured in strava-config properties file.
"""
login_strava()

"""
# STEP 2.a: Pull Data for each athlete.
Retrieves athlete information and activity data based on the provided athlete ID.

Args:
    ath_id (str): The ID of the athlete.

Returns:
    tuple: A tuple containing the athlete information and activity data.
"""


def pull_data(ath_id):
    ath_bio = get_athlete_info(ath_id.strip())
    act_ids_list = get_activity_ids(ath_id.strip())
    print(Fore.LIGHTWHITE_EX + "Total number of activity IDs collected : " + str(len(act_ids_list)))
    act_data = get_activities_data(act_ids_list)
    return ath_bio, act_data


"""
# STEP 2.b: Store Data of each athlete in the database.

    Store the athlete's biography and data in the database.

    Parameters:
        bio (str): The athlete's biography.
        data (dict): The athlete's data.

    Returns:
        None
"""


def store_in_db(bio, data):
    save_athlete_data(bio, data)


# STEP 2 : Retrieve data from strava and store it in the database.
for athlete_id in athlete_ids:
    athlete_bio, activities_data = pull_data(athlete_id)
    store_in_db(athlete_bio, activities_data)
    print(Fore.GREEN + "Data stored for athlete :" + athlete_bio[athlete_name])

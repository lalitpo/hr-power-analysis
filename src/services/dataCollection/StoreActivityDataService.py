from _datetime import datetime

from colorama import Fore

from src.constants.PowerAndHRConstants import athlete_name, athlete_id, location
from src.repositories.PowerAndHRRepository import save_record

"""
Save athlete data.

Args:
    athlete_details (dict): A dictionary containing athlete details.
    ath_act_data (list): A list of dictionaries containing athlete activity data.

Returns:
    None
"""
def save_athlete_data(athlete_details, ath_act_data):
    athlete_data = {athlete_name: athlete_details[athlete_name],
                    athlete_id: athlete_details[athlete_id],
                    location: athlete_details[location],
                    "activities_ids": [int(d['activity_id']) for d in ath_act_data if 'activity_id' in d]}
    save_record(athlete_data, "athlete-info")
    print(Fore.GREEN + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") +
          " Storing " + str(len(ath_act_data)) + " records in athletic-data in Database.")
    for data in ath_act_data:
        save_record(data, "activity-data")

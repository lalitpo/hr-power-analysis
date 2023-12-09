from src.constants.PowerAndHRConstants import athlete_name, athlete_id, location
from src.repositories.PowerAndHRRepository import save_profile_data, save_activity_data

"""
Save athlete information.

Args:
    athlete_details (dict): A dictionary containing the details of the athlete.
    ath_act_data (list): A list of dictionaries containing the athlete's activity data.

Returns:
    None
"""


def save_athlete_info(athlete_details, ath_act_data):
    athlete_data = {athlete_name: athlete_details[athlete_name],
                    athlete_id: athlete_details[athlete_id],
                    location: athlete_details[location],
                    "activities_ids": [int(d['activity_id']) for d in ath_act_data if 'activity_id' in d]}
    save_profile_data(athlete_data, "athlete-info")


"""
Save activity data to the "athletic-data" collection.

Args:
    activity_data (dict): The activity data to be saved.

Returns:
        None
"""


def save_data(activity_data):
    save_activity_data(activity_data, "athletic-data")

from src.constants.PowerAndHRConstants import athlete_name, athlete_id, location
from src.repositories.PowerAndHRRepository import save_data


def save_athlete_info(athlete_details, ath_act_data):
    athlete_data = {athlete_name: athlete_details[athlete_name], athlete_id: athlete_details[athlete_id],
                    location: athlete_details[location], "activities_ids": [int(x) for x in ath_act_data]}
    save_data(athlete_data, "athlete-info")


def save_activity_data(activity_data):
    save_data(activity_data, "athletic-data")

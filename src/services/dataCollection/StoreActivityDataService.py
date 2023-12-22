import csv
import os
from _datetime import datetime

from src.config.LoadProperties import data_folder
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
def write_to_csv(ath_name, id, activity_data):

    # Create a folder with athlete name + "_" + id
    athlete_folder = os.path.join("services/dataCollection/" + data_folder, f"{ath_name}_{id}")
    if not os.path.exists(athlete_folder):
        os.makedirs(athlete_folder)

    # Extract year and month from activity_date
    activity_date = datetime.strptime(str(activity_data["activity_date"]), "%Y-%m-%d")
    month = activity_date.month
    year = activity_date.year

    year_folder = os.path.join(athlete_folder, f"{year}")
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)

    # Create CSV file for the month
    csv_filename = os.path.join(year_folder, f"{ath_name}_{id}_{year}.csv")
    # Write data to the CSV file
    if not os.path.exists(csv_filename):
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)

            csv_writer.writerow(['activity_id', 'activity_date', 'time', 'distance', 'heartrate', 'power'])

            csv_writer.writerow([activity_data.get('activity_id', ''),
                                 activity_data.get('activity_date', ''),
                                 activity_data.get('time', ''),
                                 activity_data.get('distance', ''),
                                 activity_data.get('heartrate', ''),
                                 activity_data.get('watts', '')])

    else:
        with open(csv_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([activity_data.get('activity_id', ''),
                                 activity_data.get('activity_date', ''),
                                 activity_data.get('time', ''),
                                 activity_data.get('distance', ''),
                                 activity_data.get('heartrate', ''),
                                 activity_data.get('watts', '')])


def save_athlete_data(athlete_details, ath_act_data):
    athlete_data = {athlete_name: athlete_details[athlete_name],
                    athlete_id: athlete_details[athlete_id],
                    location: athlete_details[location],
                    "activities_ids": [int(d['activity_id']) for d in ath_act_data if 'activity_id' in d]}
    save_record(athlete_data, "athlete-info")
    for data in ath_act_data:
        # write_to_csv(athlete_data[athlete_name], athlete_data[athlete_id], data)
        save_record(data, "athletic-data")

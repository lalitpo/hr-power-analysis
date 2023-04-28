from src.services.LoginStravaService import *
import json


def get_activity_url(activity_id):
    return configs.get("strava-url").data + "/activities/" + "8943314385" + "/streams?" \
        + "stream_types%5B%5D=watts&stream_types%5B%5D=watts_calc&stream_types%5B%5D=heartrate"


activity_ids = open('../../resources/activity-id.txt')

stream_types = configs.get("stream_types").data.split(",")

for activity in activity_ids:
    url = get_activity_url(activity.strip())
    driver.get(url)
    pre = driver.find_element(By.TAG_NAME, "pre").text
    data = json.loads(pre)
    print(data)

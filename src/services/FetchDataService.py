from src.services.LoginStravaService import *
from src.repositories.PowerAndHRRepository import *
import json

stream_types = configs.get("stream_types").data.split(",")


def get_activity_url(activity_id):
    stream_types_paramlist = ""
    for param in stream_types:
        stream_types_paramlist = stream_types_paramlist + "stream_types%5B%5D=" + param + "&"
    stream_types_paramlist = stream_types_paramlist.removesuffix("$")
    return configs.get("strava-url").data + "/activities/" + activity_id + "/streams?" + stream_types_paramlist.__str__()


activity_ids = open('../../resources/activity-id.txt').readlines()

data = ""

for activity in activity_ids:
    url = get_activity_url(activity.strip())
    print(url)
    driver.implicitly_wait(10)  # latency so that strava doesn't block us for scraping using a bot.
    driver.get(url)
    pre = driver.find_element(By.TAG_NAME, "pre").text
    data = json.loads(pre)
    print(data)

store_records(data)

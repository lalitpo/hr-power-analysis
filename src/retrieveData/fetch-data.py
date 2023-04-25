from jproperties import Properties

configs = Properties()
with open('../../resources/strava-config.properties', 'rb') as config_file:
    configs.load(config_file)


def get_activity_url(activity_id):
    return configs.get("strava-url").data + "/activities/" + activity_id + "/streams?"


activity_ids = open('../../resources/activity-id.txt')

stream_types = configs.get("stream_types").data.split(",")

for activity in activity_ids:
    activity_url = get_activity_url(activity.strip())
    print(activity_url)
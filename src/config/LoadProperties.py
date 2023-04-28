from jproperties import Properties

configs = Properties()
with open('../../resources/strava-config.properties', 'rb') as strava_config:
    configs.load(strava_config)
with open('../../resources/application-config.properties', 'rb') as app_config:
    configs.load(app_config)
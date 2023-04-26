from jproperties import Properties
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

configs = Properties()
with open('../../resources/strava-config.properties', 'rb') as strava_config:
    configs.load(strava_config)
with open('../../resources/application-config.properties', 'rb') as app_config:
    configs.load(app_config)

browser_driver = '../../chromedriver'
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def login_strava(user, pwd, login_url):
    driver.get(login_url)
    username = driver.find_element(By.ID, "email")
    password = driver.find_element(By.ID, "password")
    username.send_keys(user)
    password.send_keys(pwd)
    driver.find_element(By.ID, "login-button").click()


# STEP 1 : Login into strava with Uni Account configured in properties file.
login_strava(configs.get("strava-username").data, configs.get("strava-password").data,
             configs.get("strava-login-url").data)

driver.get(configs.get("athletes-following").data)


def get_activity_url(activity_id):
    return configs.get("strava-url").data + "/activities/" + activity_id + "/streams?"


activity_ids = open('../../resources/activity-id.txt')

stream_types = configs.get("stream_types").data.split(",")

for activity in activity_ids:
    activity_url = get_activity_url(activity.strip())
    print(activity_url)

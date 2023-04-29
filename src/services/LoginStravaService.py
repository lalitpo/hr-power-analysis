from src.config.LoadProperties import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Chrome Headless Mode
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# TODO - Add options as the first argument once the application is complete and ready to fetch the data in headless mode
# No Need to download chromedriver, this installs driver everytime
# to avoid downloading manually every new patch or version of Chrome.
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

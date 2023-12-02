from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from src.config.LoadProperties import configs

# Chrome Headless Mode
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# No Need to download chromedriver,
# this installs driver everytime to avoid downloading manually every new patch or version of Chrome.
browser_driver = webdriver.Chrome(options, service=ChromeService(ChromeDriverManager().install()))


def login_strava():
    try:
        browser_driver.get(configs.get("strava-login-url").data)
        username = browser_driver.find_element(By.ID, "email")
        password = browser_driver.find_element(By.ID, "password")
        username.send_keys(configs.get("strava-username").data)
        password.send_keys(configs.get("strava-password").data)
        browser_driver.find_element(By.ID, "login-button").click()
        print("Logged in successfully to Strava.")
    except WebDriverException as webex:
        print("Login Failed : ", webex)

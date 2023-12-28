from datetime import datetime

from colorama import Fore
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By

from src.config.LoadProperties import configs


def login_strava(driver):
    try:
        print(Fore.LIGHTWHITE_EX + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Attempting to login to Strava.")
        driver.get(configs.get("strava-login-url").data)
        username = driver.find_element(By.ID, "email")
        password = driver.find_element(By.ID, "password")
        username.send_keys(configs.get("strava-username").data)
        password.send_keys(configs.get("strava-password").data)
        driver.find_element(By.ID, "login-button").click()
        print(Fore.GREEN + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Logged in successfully to Strava.")
    except WebDriverException as webex:
        print(Fore.RED + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Login Failed : ", webex)


def exit_strava(driver):
    try:
        print(Fore.LIGHTWHITE_EX + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Closing Strava session.")
        driver.close()
        driver.quit()
        print(Fore.GREEN + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Strava session closed.")
    except WebDriverException as webex:
        print(Fore.RED + (datetime.now()).strftime("%Y-%m-%d %H:%M:%S") + " Session Closing Failed : ", webex)

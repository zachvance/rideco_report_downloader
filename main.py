
"""
A downloader for RideCo reports.

TODO:
    - Program selector loop
    - Date selectors
    - Export button click
    - Wait for download
    - Loop for other reports
"""

from config import DRIVER, SITE, USERNAME, PASSWORD, REPORTS_TO_GET
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
import time


def harvest_report(driver: str, site: str, user: str, passw: str) -> None:
    """
    Opens and logs in to the site specified in config.py, with the
    credentials also specified in config.py.

    :param driver: The path of the driver to use, specified in
    config.py.
    :type driver: str
    :param site: The login page for the site, specified in config.py as
    a url string.
    :type site: str
    :param user: The username to login with, specified in config.py.
    :type user: str
    :param passw: The password to login with, specified in config.py.
    :type passw: str
    :return: None
    """

    driver = webdriver.Chrome(driver)
    driver.get(site)

    username = driver.find_element_by_id("username")
    username.clear()
    username.send_keys(user)

    password = driver.find_element_by_id("password")
    password.clear()
    password.send_keys(passw)

    driver.find_element_by_class_name("btn-login").click()


    time.sleep(2.5)
    driver.get("https://dash.sctc.rideco.com/#/exports")

    element = driver.find_element_by_id("export-select")
    for option in element.find_elements_by_tag_name('option'):
        if option.text == 'Driver Fare Export':
            option.click()  # select() in earlier versions of webdriver
            break

    print("SUCCESS")


def main():
    harvest_report(DRIVER, SITE, USERNAME, PASSWORD)


if __name__ == "__main__":
    main()
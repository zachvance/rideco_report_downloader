
"""
Docstring
"""

from config import DRIVER, SITE, USERNAME, PASSWORD
from selenium import webdriver

def site_login(driver, site, user, passw):
    """
    Opens and logs in to the site specified in config.py, with the
    credentials also specified in config.py.

    :param driver: The path of the driver to use, specified in
    config.py.
    :type driver: str
    :param site: The login page for the site, specified in config.py as
    a url string.
    :type site: str
    :param username: The username to login with, specified in config.py.
    :type username: str
    :param password: The password to login with, specified in config.py.
    :type password: str
    :return:
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

#driver.get(SITE)
#assert "rideco" in driver.title

site_login(DRIVER, SITE, USERNAME, PASSWORD)
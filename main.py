
"""
Docstring
"""

from config import DRIVER, SITE, USERNAME, PASSWORD
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select


def site_login(driver: str, site: str, user: str, passw: str) -> None:
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

    driver.get("https://dash.sctc.rideco.com/#/exports")

    form = driver.find_element_by_class_name("form-group")
    form.Select("Driver Fare Export")

    select = Select(driver.find_element_by_class_name("form-group"))
    print(select.options)
    print(o.text for o in select.options)  # these are string-s
    #select.select_by_visible_text(....)

    driver.find_element_by_css_selector("a[href=#/exports]").click()
    #driver.find_element_by_class_name("fa fa-download fa-fw").click()
    print("SUCCESS")



def main():
    site_login(DRIVER, SITE, USERNAME, PASSWORD)


if __name__ == "__main__":
    main()
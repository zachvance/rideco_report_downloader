
from config import DRIVER, SITE, USERNAME, PASSWORD
from selenium import webdriver

driver = webdriver.Chrome(DRIVER)
driver.get(SITE)
assert "rideco" in driver.title

def site_login():
    driver.get(site)
    driver.find_element_by_id(username).send_keys(USERNAME)
    driver.find_element_by_id(password).send_keys(PASSWORD)
    driver.find_element_by_id(btn-login).click()
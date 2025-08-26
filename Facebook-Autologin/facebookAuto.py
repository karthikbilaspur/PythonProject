from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service

service = Service("Facebook-Autologin/chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.facebook.com")
# add email/username instead of username@email.com
driver.find_element(By.ID, "email").send_keys("username@email.com")
# add password
driver.find_element(By.ID, "pass").send_keys("password")
driver.find_element(By.NAME, "login").click()
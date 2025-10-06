from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# LinkedIn credentials
email = "your-email@gmail.com"
password = "your-password"

# Set up the webdriver
driver = webdriver.Chrome()

def login_to_linkedin():
    driver.get("https://www.linkedin.com/login")
    username = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    username.send_keys(email)
    password_field.send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

def post_on_linkedin(post_text):
    driver.get("https://www.linkedin.com/feed/")
    post_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Start a post']"))
    )
    post_box.click()
    time.sleep(2)
    post_area = driver.find_element(By.XPATH, "//div[@aria-label='Write a post…']")
    post_area.send_keys(post_text)
    time.sleep(2)
    post_button = driver.find_element(By.XPATH, "//button[@aria-label='Post']")
    post_button.click()
    time.sleep(5)

def main():
    login_to_linkedin()
    post_text = "This is a test post from Python script."
    post_on_linkedin(post_text)
    driver.quit()

if __name__ == "__main__":
    main()
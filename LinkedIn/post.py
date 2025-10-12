from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# LinkedIn credentials
email = "your-email@gmail.com"
password = "your-password"

def setup_webdriver():
    return webdriver.Chrome()

def login_to_linkedin(driver):
    try:
        driver.get("https://www.linkedin.com/login")
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_field = driver.find_element(By.ID, "password")
        username.send_keys(email)
        password_field.send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        WebDriverWait(driver, 10).until(
            EC.url_contains("feed")
        )
    except Exception as e:
        print(f"Error logging in: {e}")

def post_on_linkedin(driver, post_text):
    try:
        driver.get("https://www.linkedin.com/feed/")
        post_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Start a post']"))
        )
        post_box.click()
        post_area = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Write a post…']"))
        )
        post_area.send_keys(post_text)
        post_button = driver.find_element(By.XPATH, "//button[@aria-label='Post']")
        post_button.click()
        time.sleep(5)
    except Exception as e:
        print(f"Error posting: {e}")

def main():
    driver = setup_webdriver()
    login_to_linkedin(driver)
    post_text = "This is a test post from Python script."
    post_on_linkedin(driver, post_text)
    driver.quit()

if __name__ == "__main__":
    main()
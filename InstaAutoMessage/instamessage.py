from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from getpass import getpass
import logging

# Set up logging
logging.basicConfig(filename='instagram_bot.log', level=logging.INFO)

# Set up Chrome driver
browser = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(browser, 120)

# Get user input
users = list(map(str, input("Enter users' usernames comma-separated whom you want to follow and send message: ").split(",")))
username = input("Enter your username: ")
password = getpass("Enter your password: ")
message = input("Write the message you want to send: ")

# Navigate to Instagram login page
try:
    browser.get('https://www.instagram.com/')
    time.sleep(2)
except Exception as e:
    logging.error(f"Failed to navigate to Instagram login page: {e}")
    browser.quit()
    exit()

# Login to Instagram
try:
    username_field = browser.find_element(By.NAME, 'username')
    username_field.send_keys(username)
    password_field = browser.find_element(By.NAME, 'password')
    password_field.send_keys(password)
    login_btn = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_btn.click()
    time.sleep(5)
except Exception as e:
    logging.error(f"Failed to login to Instagram: {e}")
    browser.quit()
    exit()

# Follow and send message to users
for user in users:
    try:
        browser.get(f"https://www.instagram.com/{user}/")
        time.sleep(3)
        follow_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//button[text()="Follow"]')))
        follow_btn.click()
        logging.info(f"Followed {user}")
        time.sleep(3)
    except Exception as e:
        logging.error(f"Failed to follow {user}: {e}")
    
    try:
        message_btn = browser.find_element(By.XPATH, '//button[text()="Message"]')
        message_btn.click()
        time.sleep(4)
        mbox = browser.find_element(By.TAG_NAME, 'textarea')
        mbox.send_keys(message)
        mbox.send_keys(Keys.RETURN)
        logging.info(f"Sent message to {user}")
        time.sleep(5)
    except Exception as e:
        logging.error(f"Failed to send message to {user}: {e}")

    # Add delay to avoid overwhelming the server
    time.sleep(10)

# Close the browser
browser.quit()
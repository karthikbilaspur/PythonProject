from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from getpass import getpass
import time

# Set up Chrome driver
chrome = webdriver.Chrome(ChromeDriverManager().install())

# Navigate to Instagram login page
chrome.get("https://instagram.com")
time.sleep(4)

# Enter username
username_input = chrome.find_element(By.NAME, "username")
username = input("Enter username: ")
username_input.send_keys(username)

# Enter password
password_input = chrome.find_element(By.NAME, "password")
password = getpass("Enter password: ")
password_input.send_keys(password)

# Click login button
login_btn = chrome.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')
login_btn.click()

# Wait for login to complete
time.sleep(5)

# Check if login was successful
if "two_factor" in chrome.current_url:
    # Handle two-factor authentication
    two_factor_input = chrome.find_element(By.NAME, "verificationCode")
    two_factor_code = input("Enter two-factor code: ")
    two_factor_input.send_keys(two_factor_code)
    two_factor_btn = chrome.find_element(By.XPATH, '//button[text()="Next"]')
    two_factor_btn.click()

# Navigate to profile page
profile_btn = chrome.find_element(By.XPATH, '//a[@href="/{}/"]'.format(username))
profile_btn.click()

# Close the browser
# chrome.quit()
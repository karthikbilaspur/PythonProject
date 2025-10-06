from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up LinkedIn credentials
email = "your_email@gmail.com"
password = "your_password"

# Set up the webdriver
driver = webdriver.Chrome()

# Navigate to LinkedIn login page
driver.get("https://www.linkedin.com/login")

# Enter login credentials
email_field = driver.find_element(By.ID, "username")
email_field.send_keys(email)
password_field = driver.find_element(By.ID, "password")
password_field.send_keys(password)
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

# Navigate to the person's profile
profile_url = "https://www.linkedin.com/in/persons-profile-url/"
driver.get(profile_url)

# Click the connect button
try:
    connect_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Connect']"))
    )
    connect_button.click()

    # Add a message if you want to
    add_note_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='You can also add a note']"))
    )
    add_note_button.click()

    # Send the invitation
    send_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send now']"))
    )
    send_button.click()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
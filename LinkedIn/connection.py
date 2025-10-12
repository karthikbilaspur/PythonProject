from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_field.send_keys(email)
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

def send_connection_request(driver, profile_url, message=""):
    driver.get(profile_url)
    try:
        connect_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Connect']"))
        )
        connect_button.click()
        
        if message:
            add_note_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add a note']"))
            )
            add_note_button.click()
            note_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[@name='message']"))
            )
            note_field.send_keys(message)
        
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send now']"))
        )
        send_button.click()
        logging.info("Connection request sent successfully")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def main():
    email = "your_email@gmail.com"
    password = "your_password"
    profile_url = "https://www.linkedin.com/in/persons-profile-url/"
    message = "Hi, I'd love to connect with you on LinkedIn!"

    driver = webdriver.Chrome()
    try:
        login(driver, email, password)
        send_connection_request(driver, profile_url, message)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

# Load environmental variables from .env file
load_dotenv()

# Read credentials from environmental variables
def read_creds():
    return {"username": os.getenv("username"), "password": os.getenv("password")}

# Function for accepting requests
def accept_requests(browser):
    browser.get("https://www.facebook.com/friends/requests")
    
    # Login to Facebook
    try:
        email_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(credentials["username"])
        
        password_input = browser.find_element(By.ID, "pass")
        password_input.send_keys(credentials["password"])
        
        login_button = browser.find_element(By.NAME, "login")
        login_button.click()
    except Exception as e:
        print(f"Error logging in: {e}")
        return
    
    # Accept friend requests
    while True:
        try:
            confirm_buttons = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Confirm']"))
            )
            if not confirm_buttons:
                break
            
            for button in confirm_buttons:
                button.click()
                time.sleep(2)
            
            # Click "See More" button
            see_more_button = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='See More']"))
            )
            see_more_button.click()
            time.sleep(5)
        except Exception as e:
            print(f"Error accepting requests: {e}")
            break

def main():
    # Initialize Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    browser = webdriver.Chrome(options=options)
    
    global credentials
    credentials = read_creds()
    accept_requests(browser)
    
    print("All friend requests accepted")
    browser.quit()

if __name__ == "__main__":
    main()

'''
Disclaimer:
This script is for educational purposes only. 
It is not intended to be used for spamming or harassing others on Facebook. 
Facebook's terms of service prohibit automating interactions on the platform without permission. 
Use this script responsibly and at your own risk. 
Be aware that Facebook may block or limit your account if it detects suspicious activity. 
Review Facebook's terms of service and usage policies before using this script.
'''    
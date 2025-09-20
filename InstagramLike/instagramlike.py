import requests
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from getpass import getpass
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstagramAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://graph.instagram.com"

    def get_user_info(self, user_id):
        url = f"{self.base_url}/{user_id}?fields=id,username&access_token={self.access_token}"
        response = requests.get(url)
        return response.json()

    def get_user_media(self, user_id):
        url = f"{self.base_url}/{user_id}/media?fields=id,caption,media_url&access_token={self.access_token}"
        response = requests.get(url)
        return response.json()

    def like_post(self, media_id):
        url = f"{self.base_url}/{media_id}/likes?access_token={self.access_token}"
        response = requests.post(url)
        return response.json()


def login(chrome):
    username = chrome.find_element(By.NAME, "username")
    username.send_keys(input("Enter your username: "))  
    password = chrome.find_element(By.NAME, "password")
    password.send_keys(getpass("Enter your password: "))
    login_button = chrome.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    login_button.click()
    time.sleep(5)

def search_user(chrome):
    search_bar = chrome.find_element(By.XPATH, "//input[@placeholder='Search']")
    search_bar.send_keys(input("Enter the username of the other person: "))
    time.sleep(2)
    search_bar.send_keys(Keys.ENTER)
    search_bar.send_keys(Keys.ENTER)
    time.sleep(2)

def like_posts(chrome):
    post = chrome.find_element(By.XPATH, "//div[@class='v1Nh3 kIKUG  _bz0w']")
    post.click()
    time.sleep(2)
    like_button = WebDriverWait(chrome, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='fr66n']//button"))
    )
    like_button.click()
    next_button = chrome.find_element(By.XPATH, "//a[text()='Next']")
    next_button.click()
    time.sleep(2)

    while True:
        try:
            like_button = WebDriverWait(chrome, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='fr66n']//button"))
            )
            like_button.click()
            next_button = chrome.find_element(By.XPATH, "//a[text()='Next']")
            next_button.click()
            time.sleep(5)
        except:
            close_button = chrome.find_element(By.XPATH, "//button[@class='ckWGn']")
            close_button.click()
            break

def main():
    choice = input("Do you want to use the Instagram API or Selenium? (api/selenium): ")
    if choice.lower() == "api":
        access_token = input("Enter your Instagram API access token: ")
        api = InstagramAPI(access_token)

        user_id = input("Enter the user ID: ")
        user_info = api.get_user_info(user_id)
        print(json.dumps(user_info, indent=4))

        user_media = api.get_user_media(user_id)
        print(json.dumps(user_media, indent=4))

        media_id = input("Enter the media ID to like: ")
        like_response = api.like_post(media_id)
        print(json.dumps(like_response, indent=4))
    elif choice.lower() == "selenium":
        chrome = webdriver.Chrome(ChromeDriverManager().install())
        chrome.get("https://www.instagram.com")
        time.sleep(2)
        login(chrome)
        search_user(chrome)
        like_posts(chrome)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
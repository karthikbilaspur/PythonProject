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
import os

class InstagramDownloader:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.chrome = webdriver.Chrome(ChromeDriverManager().install())

    def login(self):
        try:
            self.chrome.get("https://www.instagram.com")
            time.sleep(2)
            username_field = WebDriverWait(self.chrome, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(self.username)
            password_field = self.chrome.find_element(By.NAME, "password")
            password_field.send_keys(self.password)
            login_button = self.chrome.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_button.click()
            time.sleep(5)
        except Exception as e:
            print(f"Error logging in: {e}")

    def download_posts(self, user_id):
        try:
            self.chrome.get(f"https://www.instagram.com/{user_id}/")
            time.sleep(2)
            posts = WebDriverWait(self.chrome, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='v1Nh3 kIKUG  _bz0w']"))
            )
            post_urls = []
            for post in posts:
                post.click()
                time.sleep(1)
                post_url = self.chrome.current_url
                post_urls.append(post_url)
                close_button = WebDriverWait(self.chrome, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@class='ckWGn']"))
                )
                close_button.click()
                time.sleep(1)
            self.download_media(post_urls, user_id)
        except Exception as e:
            print(f"Error downloading posts: {e}")

    def download_media(self, post_urls, user_id):
        try:
            if not os.path.exists(user_id):
                os.makedirs(user_id)
            for i, post_url in enumerate(post_urls):
                self.chrome.get(post_url)
                time.sleep(1)
                try:
                    media_url = WebDriverWait(self.chrome, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//meta[@property='og:image']"))
                    ).get_attribute("content")
                    response = requests.get(media_url)
                    with open(f"{user_id}/{i+1}.jpg", "wb") as f:
                        f.write(response.content)
                except:
                    try:
                        media_url = WebDriverWait(self.chrome, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//meta[@property='og:video']"))
                        ).get_attribute("content")
                        response = requests.get(media_url)
                        with open(f"{user_id}/{i+1}.mp4", "wb") as f:
                            f.write(response.content)
                    except Exception as e:
                        print(f"Failed to download media from {post_url}: {e}")
        except Exception as e:
            print(f"Error downloading media: {e}")

def main():
    try:
        username = input("Enter your Instagram username: ")
        password = getpass("Enter your password: ")
        user_id = input("Enter the user ID: ")
        downloader = InstagramDownloader(username, password)
        downloader.login()
        downloader.download_posts(user_id)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
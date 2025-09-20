from selenium import webdriver
from time import sleep
import datetime
from prettytable import PrettyTable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.login(username, pw)

    def login(self, username, pw):
        try:
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.send_keys(username)

            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(pw)

            login_btn = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            login_btn.click()
            sleep(4)

            self.handle_save_info_prompt()
        except Exception as e:
            print(f"Error logging in: {e}")

    def handle_save_info_prompt(self):
        try:
            if self.driver.current_url == "https://www.instagram.com/accounts/onetap/?next=%2F":
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
                sleep(4)
                try:
                    self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
                except:
                    pass
            else:
                sleep(2)
                try:
                    self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
                except:
                    pass
        except Exception as e:
            print(f"Error handling save info prompt: {e}")

    def get_unfollowers(self):
        try:
            self.driver.find_element(By.XPATH, f"//a[contains(@href,'/{self.username}')]").click()
            sleep(2)
            following = self._get_names("following")
            sleep(2)
            self.driver.find_element(By.XPATH, f"//a[contains(@href,'/{self.username}/followers')]").click()
            sleep(2)
            followers = self._get_names("followers")

            not_following_back = [user for user in following if user not in followers]

            table = PrettyTable()
            table.add_column("Non-Followers", not_following_back)
            print(table)
        except Exception as e:
            print(f"Error getting unfollowers: {e}")

    def _get_names(self, section):
        try:
            sleep(2)
            scroll_box = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[2]")
            last_ht, ht = 0, 1

            while last_ht != ht:
                last_ht = ht
                sleep(1)
                ht = self.driver.execute_script(
                    """
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)

            links = scroll_box.find_elements(By.TAG_NAME, 'a')
            names = [name.text for name in links if name.text != '']

            sleep(1)

            close_btn = self.driver.find_element(By.XPATH, "/html/body/div[5]/div/div/div[1]/div/div[2]")
            close_btn.click()

            return names
        except Exception as e:
            print(f"Error getting {section} names: {e}")


def main():
    usr_name = input("Enter Username: ")
    password = input("Enter Password: ")

    my_bot = InstaBot(usr_name, password)
    my_bot.get_unfollowers()


if __name__ == "__main__":
    main()
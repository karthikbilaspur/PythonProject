# Selenium is required for automation
# sleep is required to have some time for scanning
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def whatsapp(to: str, message: str) -> None:
    """
    Send a WhatsApp message to a contact.

    Args:
        to (str): The name of the contact to send the message to.
        message (str): The message to send.

    Returns:
        None
    """
    # Set up Chrome driver
    chrome_driver_binary = "C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_binary)
    driver.get("https://web.whatsapp.com/")
    logging.info("Waiting for QR code scan...")
    sleep(15)  # Wait for QR code scan

    try:
        # Find the contact
        user = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@title='{}']".format(to)))
        )
        user.click()
        logging.info("Contact found and selected.")

        # Send the message
        text_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        text_box.send_keys(message)
        send_button = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div[3]/button')
        send_button.click()
        logging.info("Message sent successfully.")
    except Exception as e:
        logging.error("Error occurred: {}".format(e))
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    to = input('Who do you want to send a message to? Enter the name: ')
    content = input("What message do you want to send? Enter the message: ")
    whatsapp(to, content)
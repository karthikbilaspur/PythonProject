
import pywhatkit
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WhatsApp Auto Messenger
phoneno = input("Enter Receiver(recipient) Phone Number (with country code, e.g., +91XXXXXXX): ")
message = input("Enter Message You want to send :")
print("Enter Schedule Time to send WhatsApp message to recipient :")
Time_hrs = int(input("- At What Hour (24-hour format, e.g., 14): "))
Time_min = int(input("- At What Minutes : "))
pywhatkit.sendwhatmsg(phoneno, message, Time_hrs, Time_min, wait_time=20, tab_close=True, close_time=2)# Website Automation
driver = webdriver.Chrome()
driver.get("https://www.example.com")

# Find the search input field
search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "q"))
)

# Enter the search query
search_input.send_keys("python")

# Website Automation with Selenium
def automate_website(url: str) -> None:
    driver = webdriver.Chrome()
    driver.get(url)

    # Find the search input field
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # Enter the search query
    search_input.send_keys("python")

    # Find the search button
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "btnK"))
    )

    # Click the search button
    search_button.click()

    # Close the browser
    driver.quit()

# Call the function
url = input("Enter website URL: ")
automate_website(url)
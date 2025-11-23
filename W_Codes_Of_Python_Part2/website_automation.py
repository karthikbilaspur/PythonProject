from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the browser
driver = webdriver.Chrome()

# Navigate to the website
driver.get("https://www.example.com")

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
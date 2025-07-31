from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a new instance of the Chrome driver with options
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Navigate to a URL
driver.get("https://www.example.com")

# Wait for an element to be present
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "my_element"))
)

# Close the driver
driver.quit()
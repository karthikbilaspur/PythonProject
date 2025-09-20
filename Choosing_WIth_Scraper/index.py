import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
import logging
from fake_useragent import UserAgent
import random

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_website(url):
    try:
        # Create a UserAgent object
        ua = UserAgent()
        
        # Generate a random user-agent
        user_agent = ua.random
        
        # Set up headers with the user-agent
        headers = {
            'User-Agent': user_agent
        }
        
        # Send a GET request with the headers
        response = requests.get(url, headers=headers, timeout=10)
        
        # If the GET request is successful, the status code will be 200
        if response.status_code == 200:
            # Get the content of the response
            page_content = response.content
            
            # Create a BeautifulSoup object and specify the parser
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Find the elements you want to scrape
            titles = soup.find_all(['h1', 'h2', 'h3'])
            links = soup.find_all('a')
            images = soup.find_all('img')
            
            # Create lists to store the scraped data
            title_list = [title.text.strip() for title in titles]
            link_list = [link.get('href') for link in links if link.get('href')]
            image_list = [image.get('src') for image in images if image.get('src')]
            
            # Create DataFrames to store the scraped data
            df_titles = pd.DataFrame(title_list, columns=['Titles'])
            df_links = pd.DataFrame(link_list, columns=['Links'])
            df_images = pd.DataFrame(image_list, columns=['Images'])
            
            # Save the DataFrames to CSV files
            df_titles.to_csv('scraped_titles.csv', index=False)
            df_links.to_csv('scraped_links.csv', index=False)
            df_images.to_csv('scraped_images.csv', index=False)
            
            logging.info("Data scraped successfully!")
            print("Data scraped successfully!")
        else:
            logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")

def job():
    url = "http://example.com"
    scrape_website(url)

# Schedule the job to run every day at 8am
schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
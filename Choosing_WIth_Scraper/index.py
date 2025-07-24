import requests
from bs4 import BeautifulSoup
import pandas as pd
import schedule
import time
import logging
from fake_useragent import UserAgent
import random

# Set up logging
logging.basicConfig(filename='scraper.log', level=logging.INFO)

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
        response = requests.get(url, headers=headers)
        
        # If the GET request is successful, the status code will be 200
        if response.status_code == 200:
            # Get the content of the response
            page_content = response.content
            
            # Create a BeautifulSoup object and specify the parser
            soup = BeautifulSoup(page_content, 'html.parser')
            
            # Find the elements you want to scrape
            titles = soup.find_all('h2')
            links = soup.find_all('a')
            
            # Create lists to store the scraped data
            title_list = []
            link_list = []
            
            # Loop through the elements and extract the data
            for title in titles:
                title_list.append(title.text.strip())
                
            for link in links:
                link_list.append(link.get('href'))
                
            # Create a DataFrame to store the scraped data
            df = pd.DataFrame({
                'Title': title_list,
                'Link': link_list
            })
            
            # Save the DataFrame to a CSV file
            df.to_csv('scraped_data.csv', index=False)
            
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
import requests
from bs4 import BeautifulSoup

def scrape_data(url):
    """
    Scrapes the title and paragraph texts from a given webpage.
    
    Args:
        url (str): The URL of the webpage to scrape.
    
    Returns:
        A dictionary containing the title and paragraph texts.
    """
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the title
            title = soup.title.text
            
            # Extract all paragraph texts
            paragraphs = [p.text for p in soup.find_all('p')]
            
            # Return the scraped data
            return {
                'title': title,
                'paragraphs': paragraphs
            }
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

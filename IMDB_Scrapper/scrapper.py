# Import necessary libraries
import requests
from bs4 import BeautifulSoup

# Function to scrape IMDB top movies
def scrape_imdb_top_movies(url):
    """
    Scrapes movie titles and ratings from the given IMDB page.
    
    Args:
        url (str): URL of the IMDB page to scrape.
    """
    
    # Define headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all movie rows
        movies = soup.find_all('tr')
        
        # Iterate over the movie rows (skipping the header row)
        for movie in movies[1:]:  
            # Find the title and rating columns
            title_column = movie.find('td', class_='titleColumn')
            rating_column = movie.find('td', class_='imdbRating')
            
            # Check if both columns exist
            if title_column and rating_column:
                # Extract the title and rating
                title = title_column.a.text
                rating = rating_column.strong.text
                
                # Print the movie details
                print(f"Title: {title}, Rating: {rating}")
                
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# URL of the IMDB top 250 movies page
url = "https://www.imdb.com/chart/top/"
scrape_imdb_top_movies(url)
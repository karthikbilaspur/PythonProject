# Book Scraper

This script is a web scraper designed to extract book information from the website "Books to Scrape". Here's a breakdown:
Key Features:
Scrapes book data: Extracts title, price, rating, and description for each book
Handles categories: Can scrape books from specific categories or all categories
Saves to CSV: Saves the scraped data to a CSV file
How it Works:
Gets categories: If no category is specified, the script extracts all categories from the website
Scrapes book data: Iterates through each category and page, extracting book information
Saves data: Saves the scraped data to a CSV file
Main Functions:
scrape_books: Scrapes book data from the website
get_categories: Extracts categories from the website
extract_book_info: Extracts information for a single book
save_to_csv: Saves the scraped data to a CSV file.

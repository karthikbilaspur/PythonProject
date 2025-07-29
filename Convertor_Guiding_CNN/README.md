# CNN Article Scraper Summary

This Python script scrapes CNN articles using BeautifulSoup and requests libraries. Here's a breakdown of the script:
Steps:
Fetch CNN Homepage HTML: Retrieves the HTML content of the CNN homepage.
Extract Article Links: Extracts all links from the homepage and filters out non-article links.
Filter Article URLs: Filters article links based on the current year and excludes gallery links.
Scrape Article Details: Scrapes title, author, and article content from each article link.
Save Data to Excel: Saves the scraped data to an Excel file named "cnn_articles.xlsx".
Key Functions:
url_is_article(url, current_year='2023'): Filters article URLs based on the current year.
parse(html): Scrapes title, author, and article content from an article's HTML.
Output:
An Excel file named "cnn_articles.xlsx" containing the scraped article data, including:
Title
Author
Article Text
Notes:
The script uses a specific year (2023) to filter article URLs. You may need to update this value to scrape articles from different years.
The script assumes that the article content is contained within a div element with the class article__content. If the website structure changes, you may need to update the script accordingly.

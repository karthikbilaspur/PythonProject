import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from fpdf import FPDF

# Get input for topic and number of articles
topic = input("Enter topic: ")
number_articles = int(input("Enter number of articles: "))
driver_path = input("Enter chrome driver path: ")

url = f'https://medium.com/search?q={topic}'

# Initiating the webdriver
driver = webdriver.Chrome(driver_path)
driver.get(url)

# Ensure the page is loaded
time.sleep(5)
html = driver.page_source

# Apply BeautifulSoup to html
soup = BeautifulSoup(html, "html.parser")
articles = soup.find_all('div', class_='section-content')

# Extracting articles from Medium
count = 0
for article in articles:
    try:
        link = article.find('a')['href']
        if link.startswith('https://medium.com/'):
            article_url = link
        else:
            article_url = f'https://medium.com{link}'

        driver.get(article_url)
        time.sleep(5)

        article_html = driver.page_source
        article_soup = BeautifulSoup(article_html, "html.parser")

        # Extract title
        title = article_soup.find('title').text.strip()

        # Extract content
        content = article_soup.find_all('p')
        article_content = '\n\n'.join([p.text.strip() for p in content])

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=title, ln=1, align='C')
        pdf.multi_cell(0, 5, txt=article_content, align='L')

        # Save PDF
        pdf_title = ''.join(e for e in title if e.isalnum())
        pdf.output(f"{pdf_title}.pdf")

        count += 1
        if count == number_articles:
            break
    except Exception as e:
        print(f"Error: {e}")

driver.close()
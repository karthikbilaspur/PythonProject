import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fetch CNN homepage HTML
url = 'https://www.cnn.com'
data = requests.get(url).text
soup = BeautifulSoup(data, features="html.parser")

# Extract article links
all_urls = []
for a in soup.find_all('a', href=True):
    if a['href'] and a['href'][0] == '/' and a['href'] != '#':
        a['href'] = url + a['href']
        all_urls.append(a['href'])

# Filter article URLs
def url_is_article(url, current_year='2025'):
    if url:
        if 'cnn.com/{}/'.format(current_year) in url and '/gallery/' not in url:
            return True
    return False

article_urls = [url for url in all_urls if url_is_article(url)]

# Scrape article details
def parse(html):
    soup = BeautifulSoup(html, features="html.parser")
    title = soup.find('h1', {'class': 'headline__text'})
    if title:
        title = title.text.strip()
    else:
        title = ''
    author = soup.find('span', {'class': 'byline__name'})
    if not author:
        author = soup.find('span', {'class': 'byline__names'})
    author = author.text.strip() if author else ''
    article_content = soup.find('div', {'class': 'article__content'})
    if article_content:
        article_content = article_content.text.strip()
    else:
        article_content = ''
    return title, author, article_content

all_data = []
for article_url in article_urls:
    article_data = requests.get(article_url).text
    parsed_data = parse(article_data)
    all_data.append(parsed_data)

# Save data to Excel
df = pd.DataFrame(all_data, columns=['Title', 'Author', 'Article Text'])
df.to_excel('cnn_articles.xlsx', index=False)
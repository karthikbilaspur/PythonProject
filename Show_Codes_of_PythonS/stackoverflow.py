import requests
from bs4 import BeautifulSoup, Tag
import pandas as pd
import time
import random

# Define a function to scrape questions
def scrape_questions(tag: str, pages: int=1, delay: float=1.0) -> list[dict[str, str]]:
    questions: list[dict[str, str]] = []
    for page in range(1, pages+1):
        url = f'https://stackoverflow.com/questions/tagged/{tag}?tab=newest&page={page}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        question_elements = soup.find_all('div', class_='question-summary')
        for question_element in question_elements:
            try:
                if not isinstance(question_element, Tag):
                    continue
                h3_tag = question_element.find('h3')
                if not isinstance(h3_tag, Tag):
                    continue
                a_tag = h3_tag.find('a')
                if not isinstance(a_tag, Tag):
                    continue
                votes_tag = question_element.find('span', class_='vote-count-post')
                status_tag = question_element.find('div', class_='status')
                views_tag = question_element.find('div', class_='views')
                asked_tag = question_element.find('span', class_='relativetime')
                
                href = a_tag.get('href')
                # normalize BeautifulSoup attribute that can be a list or None to a string
                if isinstance(href, list):
                    href = href[0] if href else ''
                href = href or ''
                question = {
                    'title': h3_tag.get_text(strip=True),
                    'link': 'https://stackoverflow.com' + href,
                    'votes': votes_tag.get_text(strip=True) if isinstance(votes_tag, Tag) else '',
                    'answers': status_tag.get_text(strip=True) if isinstance(status_tag, Tag) else '',
                    'views': views_tag.get_text(strip=True) if isinstance(views_tag, Tag) else '',
                    'tags': [t.get_text(strip=True) for t in question_element.find_all('a', class_='post-tag')],
                    'asked': asked_tag.get_text(strip=True) if isinstance(asked_tag, Tag) else ''
                }
                questions.append(question)
            except Exception as e:
                print(f"Error parsing question: {e}")
        # Add a random delay to avoid overwhelming the server
        time.sleep(delay + random.uniform(0, 1))
    return questions

# Scrape questions
tag = 'python'
pages = 2
questions = scrape_questions(tag, pages)

# Save to CSV
df = pd.DataFrame(questions)
df.to_csv(f'{tag}_questions.csv', index=False)

# Print questions
for question in questions:
    print(question['title'])
    print(question['link'])
    print(f"Votes: {question['votes']}, Answers: {question['answers']}, Views: {question['views']}")
    print(f"Tags: {', '.join(question['tags'])}")
    print(f"Asked: {question['asked']}")
    print('---')
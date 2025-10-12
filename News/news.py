import io
import os
import sys
from contextlib import contextmanager
import requests
from bs4 import BeautifulSoup
import csv

import newsapi
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

more_news = True
article_number = 0

def fetch_news() -> dict:
    query = input("What do you want to hear about? ")
    return newsapi.get_everything(q=query)

def get_top_ten_news(category):
    URL = "https://www.indiatoday.in/"
    category_url = URL + category
    page = requests.get(category_url)
    soup = BeautifulSoup(page.text, "html.parser")
    
    top_ten_news = []
    count = 0
    
    all_div_tags = soup.find_all(class_="detail")
    for div in all_div_tags:
        count += 1
        if count > 10:
            break
        headline = div.find("h2").text
        link = div.find("a").attrs["href"]
        top_ten_news.append([headline, link])
    
    return top_ten_news

def speak(text: str):
    with io.BytesIO() as f:
        gTTS(text=text, lang='en').write_to_fp(f)
        f.seek(0)
        audio = AudioSegment.from_file(f, format="mp3")
        play(audio)

def main():
    global newsapi
    with open("api_key.txt", "r") as file:
        api_key = file.readline()
    newsapi = newsapi.NewsApiClient(api_key=api_key)

    categories = ["india", "world", "cities", "business", "health", "technology", "sports", "education", "lifestyle"]
    print("Please Choose a Category from the following list")
    for index, category in enumerate(categories):
        print(str(index + 1) + ". " + category.capitalize())
    print("Example: Enter 'world' for top 10 world news")
    category = input().lower()

    if category in categories:
        top_ten_news = get_top_ten_news(category)
        for news in top_ten_news:
            print(news[0])
            speak(news[0])
            print("Read more at https://www.indiatoday.in/" + news[1])
    else:
        headlines = fetch_news()
        while more_news:
            global article_number
            article_number += 1
            try:
                article = headlines["articles"][article_number]
                print(article["title"], "-", article["source"]["name"])
                speak(article["title"])
                print(article["description"])
                speak(article["description"])
                print("Continue reading on this URL:", article["source"]["name"])
            except IndexError:
                speak("It looks like there are no more news on this topic. Why not search something else? ")
            except KeyboardInterrupt:
                break
            if article_number == 10:
                article_number = 0
                if input("Want to hear more news? [y/n] ") != "y":
                    global more_news
                    more_news = False

if __name__ == "__main__":
    main()
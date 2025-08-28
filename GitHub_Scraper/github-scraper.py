import requests
from bs4 import BeautifulSoup
import json

def scrape_github_user(username):
    url = f"https://github.com/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        user_info = {}

        # Scrape username
        user_info["username"] = username

        # Scrape name
        name_element = soup.find("span", {"class": "p-name vcard-fullname d-block overflow-hidden"})
        if name_element:
            user_info["name"] = name_element.text.strip()
        else:
            user_info["name"] = None

        # Scrape bio
        bio_element = soup.find("div", {"class": "p-note user-profile-bio mb-3 js-user-profile-bio f4"})
        if bio_element:
            user_info["bio"] = bio_element.text.strip()
        else:
            user_info["bio"] = None

        # Scrape location
        location_element = soup.find("li", {"itemprop": "homeLocation"})
        if location_element:
            user_info["location"] = location_element.text.strip()
        else:
            user_info["location"] = None

        # Scrape followers and following
        followers_element = soup.find("a", {"href": f"/{username}?tab=followers"})
        following_element = soup.find("a", {"href": f"/{username}?tab=following"})
        if followers_element and following_element:
            user_info["followers"] = followers_element.text.strip().split()[0]
            user_info["following"] = following_element.text.strip().split()[0]
        else:
            user_info["followers"] = None
            user_info["following"] = None

        return user_info
    else:
        return None

def main():
    username = input("Enter GitHub username: ")
    user_info = scrape_github_user(username)
    if user_info:
        print(json.dumps(user_info, indent=4))
    else:
        print("Failed to scrape user information.")

if __name__ == "__main__":
    main()
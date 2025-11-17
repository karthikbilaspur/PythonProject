import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Optional

class TechCrunchError(Exception):
    """Base class for TechCrunch exceptions."""
    pass

class TechCrunchRequestError(TechCrunchError):
    """Raised when a request to TechCrunch fails."""
    pass
and
class TechCrunchParseError(TechCrunchError):
    """Raised when parsing of TechCrunch data fails."""
    pass

class TechCrunch:
    """
    Class - `TechCrunch`
    Example:
    ```
    articles = TechCrunch()
    ```\n
    Methods :\n
    1. ``.getArticles() | Response - Articles with title, descriptions, images, date and link.
    2. ``.search() | Response - Articles with title, descriptions, images, date and link based on search topic.
    """

    def __init__(self):
        self.base_url = "https://techcrunch.com"
        self.search_url = "https://search.techcrunch.com/search"

    def _get_soup(self, url: str) -> Optional[BeautifulSoup]:
        try:
            res = requests.get(url)
            res.raise_for_status()
            return BeautifulSoup(res.text, "html.parser")
        except requests.RequestException as e:
            raise TechCrunchRequestError(f"Failed to retrieve data from {url}: {e}")

    def _extract_article_data(self, article: BeautifulSoup) -> Dict[str, str]:
        try:
            title_elem = article.select_one(".post-block__title__link")
            name = title_elem.getText().strip().encode("ascii", "ignore").decode() if title_elem else ""
            desc_elem = article.select_one(".post-block__content")
            desc = desc_elem.getText().strip().encode("ascii", "ignore").decode() if desc_elem else ""
            images = article.find_all("img", src=True)
            image = str(images[0]["src"]) if images else ""
            author_elem = article.select_one(".river-byline__authors")
            author = author_elem.getText().strip().encode("ascii", "ignore").decode() if author_elem else ""
            date_elem = article.select_one(".river-byline__time")
            date = date_elem.getText().strip().encode("ascii", "ignore").decode() if date_elem else ""
            links = article.find_all("a", class_="post-block__title__link", href=True)
            link = links[0]["href"] if links else ""
            return {
                "title": name,
                "description": desc,
                "image": image,
                "author": author,
                "date": date,
                "link": link,
            }
        except Exception as e:
            raise TechCrunchParseError(f"Failed to extract article data: {e}")

    def _extract_search_article_data(self, article: BeautifulSoup) -> Dict[str, str]:
        try:
            name = article.find("a", class_="fz-20 lh-22 fw-b").getText()
            desc = article.find("p", class_="fz-14 lh-20 c-777").getText()
            image = article.find("img", class_="s-img mr-10 s-img-errchk", src=True)["src"]
            author = article.find("span", class_="mr-15").getText()
            date = article.find("span", class_="pl-15 bl-1-666").getText()
            link = article.find("a", class_="fz-20 lh-22 fw-b", href=True)["href"]
            return {
                "title": name,
                "description": desc,
                "image": image,
                "author": author,
                "date": date,
                "link": link,
            }
        except Exception as e:
            raise TechCrunchParseError(f"Failed to extract search article data: {e}")

    def get_articles(self, category: str) -> str:
        """
        Class - `TechCrunch`
        Example:
        ```
        articles = TechCrunch()
        articles.getArticles("artificial-intelligence")
        ```
        Returns:
        {
            "title": Tile of the article
            "description": Description of the article
            "image": Image of the article
            "author": Author of the Article
            "date": Date the article was posted
            "link": Link to the article
        }
        """
        try:
            url = f"{self.base_url}/category/{category.replace(' ', '-').lower()}"
            soup = self._get_soup(url)
            articles = soup.find_all("div", class_="post-block post-block--image post-block--unread")
            articles_data = [self._extract_article_data(article) for article in articles]
            return json.dumps({"articles": articles_data})
        except TechCrunchError as e:
            return json.dumps({"error": str(e)})

    def search(self, topic: str) -> str:
        """
        Class - `TechCrunch`
        Example:
        ```
        articles = TechCrunch()
        articles.search("github")
        ```
        Returns:
        {
            "title": Tile of the article
            "description": Description of the article
            "image": Image of the article
            "author": Author of the Article
            "date": Date the article was posted
            "link": Link to the article
        }
        """
        try:
            url = f"{self.search_url}?p={topic}&fr=techcrunch"
            soup = self._get_soup(url)
            articles = soup.find_all("li", class_="ov-a mt-0 pt-26 pb-26 bt-dbdbdb")
            articles_data = [self._extract_search_article_data(article) for article in articles]
            return json.dumps({"articles": articles_data})
        except TechCrunchError as e:
            return json.dumps({"error": str(e)})
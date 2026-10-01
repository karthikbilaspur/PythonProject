import requests
from bs4 import BeautifulSoup
from typing import Any, Callable, Optional

try:
    from ratelimit import limits, sleep_and_retry
except ImportError:  # pragma: no cover
    def sleep_and_retry(func: Callable[..., Any]) -> Callable[..., Any]:
        return func

    def limits(calls: int, period: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            return func
        return decorator

try:
    from fake_useragent import UserAgent
except ImportError:  # pragma: no cover
    class UserAgent:
        @property
        def random(self) -> str:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"


class Product:
    def __init__(self, product_name: str):
        self.product_name: str = product_name
        self.ua = UserAgent()
        self.headers: dict[str, str] = {
            "User-Agent": self.ua.random
        }

    @sleep_and_retry
    @limits(calls=10, period=60)
    def send_request(self, url: str) -> Optional[requests.Response]:
        try:
            response = requests.get(url, headers=self.headers, timeout=20)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_product(self) -> dict[str, Any]:
        try:
            product_name = self.product_name.replace(" ", "+")
            url = f"https://www.amazon.in/s?k={product_name}"
            response = self.send_request(url)
            if response is None:
                return {"data": None, "message": "Unable to fetch product links: response was None"}

            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.find_all("div", {"class": "s-product-image-container"})
            product_links: list[str] = []
            for product in products:
                link_tag = product.find("a", {"class": "a-link-normal"})
                if link_tag is None or not link_tag.get("href"):
                    continue
                href = link_tag["href"]
                if href.startswith("/"):
                    href = "https://www.amazon.in" + href
                product_links.append(href)
            return {
                "data": product_links,
                "message": "Product links have been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product links: {e}",
            }

    def get_product_details(self, product_link: str) -> dict[str, Any]:
        try:
            response = self.send_request(product_link)
            if response is None:
                return {"data": None, "message": "Unable to fetch product detail: response was None"}

            soup = BeautifulSoup(response.content, "html.parser")
            product_name_tag = soup.find("span", {"id": "productTitle"})
            product_price_tag = soup.find("span", {"class": "a-price-whole"})
            product_rating_tag = soup.find("span", {"class": "a-size-base a-color-base"})

            product_name = product_name_tag.get_text(strip=True) if product_name_tag else "N/A"
            product_price = product_price_tag.get_text(strip=True) if product_price_tag else "N/A"
            product_rating = product_rating_tag.get_text(strip=True) if product_rating_tag else "N/A"

            product_details = {
                "product_name": product_name,
                "product_price": product_price,
                "product_rating": product_rating,
                "product_link": product_link,
            }
            return {
                "data": product_details,
                "message": "Product detail has been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product detail: {e}",
            }

    def get_product_image(self, product_link: str) -> dict[str, Any]:
        try:
            response = self.send_request(product_link)
            if response is None:
                return {"data": None, "message": "Unable to fetch product image: response was None"}

            soup = BeautifulSoup(response.content, "html.parser")
            image_tag = soup.find("img", {"class": "a-dynamic-image a-stretch-horizontal"})
            product_image = image_tag["src"] if image_tag and image_tag.get("src") else "N/A"
            return {
                "data": product_image,
                "message": "Product image has been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product image: {e}",
            }

    def customer_review(self, product_link: str) -> dict[str, Any]:
        try:
            response = self.send_request(product_link)
            if response is None:
                return {"data": None, "message": "Unable to fetch product reviews: response was None"}

            soup = BeautifulSoup(response.content, "html.parser")
            review_elements = soup.find_all("div", {"data-hook": "review"})
            reviews: list[dict[str, str]] = []
            for review_element in review_elements:
                reviewer_name_tag = review_element.find("span", {"class": "a-profile-name"})
                rating_star = review_element.find("i", {"class": "a-icon-star"})
                rating_tag = rating_star.find("span", {"class": "a-icon-alt"}) if rating_star else None
                review_title_tag = review_element.find("a", {"data-hook": "review-title"})
                review_date_tag = review_element.find("span", {"data-hook": "review-date"})
                review_text_tag = review_element.find("span", {"data-hook": "review-body"})

                reviewer_name = reviewer_name_tag.get_text(strip=True) if reviewer_name_tag else "N/A"
                rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"
                review_title = review_title_tag.get_text(strip=True) if review_title_tag else "N/A"
                review_date = review_date_tag.get_text(strip=True) if review_date_tag else "N/A"
                review_text = review_text_tag.get_text(strip=True) if review_text_tag else "N/A"

                review = {
                    "reviewer_name": reviewer_name,
                    "rating": rating,
                    "review_title": review_title,
                    "review_date": review_date,
                    "review_text": review_text,
                }
                reviews.append(review)
            return {
                "data": reviews,
                "message": "Product reviews have been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product reviews: {e}",
            }


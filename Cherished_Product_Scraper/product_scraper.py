import requests
from bs4 import BeautifulSoup
import random
from ratelimit import limits, sleep_and_retry
from fake_useragent import UserAgent

class Product:
    def __init__(self, product_name: str):
        self.product_name = product_name
        self.ua = UserAgent()
        self.headers = {
            "User-Agent": self.ua.random
        }

    @sleep_and_retry
    @limits(calls=10, period=60)
    def send_request(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get_product(self):
        try:
            product_name = self.product_name
            product_name = product_name.replace(" ", "+")
            url = f"https://www.amazon.in/s?k={product_name}"
            response = self.send_request(url)
            soup = BeautifulSoup(response.content, "html.parser")
            products = soup.find_all("div", {"class": "s-product-image-container"})
            product_links = []
            for product in products:
                product_link = product.find("a", {"class": "a-link-normal"})["href"]
                product_links.append("https://www.amazon.in" + product_link)
            return {
                "data": product_links,
                "message": f"Product links have been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product links: {e}",
            }

    def get_product_details(self, product_link):
        try:
            response = self.send_request(product_link)
            soup = BeautifulSoup(response.content, "html.parser")
            product_name = soup.find("span", {"id": "productTitle"}).text.strip()
            product_price = soup.find("span", {"class": "a-price-whole"}).text.strip()
            product_rating = soup.find("span", {"class": "a-size-base a-color-base"}).text.strip()
            product_details = {
                "product_name": product_name,
                "product_price": product_price,
                "product_rating": product_rating,
                "product_link": product_link,
            }
            return {
                "data": product_details,
                "message": f"Product detail has been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product detail: {e}",
            }

    def get_product_image(self, product_link):
        try:
            response = self.send_request(product_link)
            soup = BeautifulSoup(response.content, "html.parser")
            product_image = soup.find("img", {"class": "a-dynamic-image a-stretch-horizontal"})["src"]
            return {
                "data": product_image,
                "message": f"Product image has been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product image: {e}",
            }

    def customer_review(self, product_link):
        try:
            response = self.send_request(product_link)
            soup = BeautifulSoup(response.content, "html.parser")
            review_elements = soup.find_all("div", {"data-hook": "review"})
            reviews = []
            for review_element in review_elements:
                reviewer_name = review_element.find("span", {"class": "a-profile-name"}).text
                rating = review_element.find("i", {"class": "a-icon-star"}).find("span", {"class": "a-icon-alt"}).text
                review_title = review_element.find("a", {"data-hook": "review-title"}).text.strip()
                review_date = review_element.find("span", {"data-hook": "review-date"}).text
                review_text = review_element.find("span", {"data-hook": "review-body"}).text.strip()
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
                "message": f"Product reviews have been fetched",
            }
        except Exception as e:
            return {
                "data": None,
                "message": f"Unable to fetch product reviews: {e}",
            }


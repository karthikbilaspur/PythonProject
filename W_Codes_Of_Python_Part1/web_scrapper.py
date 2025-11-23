import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_magicbricks(url: str) -> pd.DataFrame:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")
    properties = soup.find_all("div", attrs={"class": "mb-srp__list"})

    data = []
    for property in properties:
        price = property.find("div", attrs={"class": "mb-srp__card__price--amount"})
        title = property.find("h2", attrs={"class": "mb-srp__card--title"})
        summary_values = property.find_all("div", attrs={"class": "mb-srp__card__summary--value"})
        status = property.find("span", attrs={"class": "mb-srp__card__summary--value"})
        property_age = property.find("div", attrs={"class": "mb-srp__card__age"})

        data.append({
            "Price": price.text.strip() if price else "Not specified",
            "Title": title.text.strip() if title else "Not specified",
            "Carpet Area": summary_values[0].text.strip() if summary_values else "Not specified",
            "Status": status.text.strip() if status else "Not specified",
            "Overlooking": summary_values[1].text.strip() if len(summary_values) > 1 else "Not specified",
            "Property Age": property_age.text.strip() if property_age else "Not specified",
        })

    return pd.DataFrame(data)

url = "https://www.magicbricks.com/flats-in-kolkata-for-sale-pppfs"
df = scrape_magicbricks(url)
print(df)
import requests
import json

class PageSpeedAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    def get_pagespeed_results(self, url, strategy="desktop", category=None):
        params = {
            "url": url,
            "key": self.api_key,
            "strategy": strategy
        }

        if category:
            params["category"] = category

        response = requests.get(self.base_url, params=params)
        return response.json()

    def save_pagespeed_results(self, url, strategy="desktop", category=None, output_file="pagespeed_results.json"):
        results = self.get_pagespeed_results(url, strategy, category)
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
        return results

def main():
    api_key = "YOUR_API_KEY"  # Replace with your PageSpeed API key
    pagespeed = PageSpeedAPI(api_key)

    url = input("Enter the website URL: ")
    strategy = input("Enter the strategy (desktop/mobile): ")
    category = input("Enter the category (optional): ")

    if category.strip() == "":
        category = None

    results = pagespeed.save_pagespeed_results(url, strategy, category)
    print("PageSpeed results saved to pagespeed_results.json")

if __name__ == "__main__":
    main()
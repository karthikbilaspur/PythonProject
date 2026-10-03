from google_play_scraper import app
import pandas as pd

def scrape_app_data(package_name: str) -> pd.DataFrame:
    try:
        # Scrape app data
        result = app(
            package_name,
            lang='en',  # English
            country='us'  # United States
        )

        # Extract relevant data
        data = {
            'Title': [result['title']],
            'Package Name': [result['appId']],
            'Rating': [result['score']],
            'Reviews': [result['reviews']],
            'Installs': [result['installs']],
            'Version': [result['version']],
            'Developer': [result['developer']]
        }

        # Create a DataFrame
        df = pd.DataFrame(data)

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    package_name = input("Enter the package name of the app: ")
    df = scrape_app_data(package_name)

    if df is not None:
        print(df)
        df.to_csv('app_data.csv', index=False)
        print("App data saved to app_data.csv")

if __name__ == "__main__":
    main()
import time
import logging
import argparse
import os
from typing import List
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Optional dependencies with safe fallbacks ---
try:
    import schedule
except ImportError:
    schedule = None

try:
    from fake_useragent import UserAgent
    def get_ua():
        return UserAgent().random
except ImportError:
    def get_ua():
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"

# --- Logging to both file and console ---
os.makedirs("data", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/scraper.log'),
        logging.StreamHandler()
    ]
)

def scrape_website(url: str, output_dir: str = "data") -> bool:
    try:
        headers = {
            'User-Agent': get_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

        logging.info(f"Scraping {url}")
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract with cleaning
        titles = [t.get_text(strip=True) for t in soup.find_all(['h1', 'h2', 'h3']) if t.get_text(strip=True)]
        
        # Resolve relative URLs to absolute
        links = []
        for a in soup.find_all('a', href=True):
            href = a.get('href').strip()
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            links.append(urljoin(url, href))
        
        images = []
        for img in soup.find_all('img', src=True):
            src = img.get('src').strip()
            images.append(urljoin(url, src))

        # Deduplicate while keeping order
        titles = list(dict.fromkeys(titles))
        links = list(dict.fromkeys(links))
        images = list(dict.fromkeys(images))

        # Save as ONE combined report + separate files
        timestamp = pd.Timestamp.now().strftime("%Y-%m-%d")

        # Combined CSV for analysis
        max_len = max(len(titles), len(links), len(images), 1)
        df_combined = pd.DataFrame({
            'Titles': titles + ['']*(max_len-len(titles)),
            'Links': links + ['']*(max_len-len(links)),
            'Images': images + ['']*(max_len-len(images)),
        })
        df_combined.to_csv(f"{output_dir}/scraped_report_{timestamp}.csv", index=False)
        
        # Separate files too
        pd.DataFrame(titles, columns=['Titles']).to_csv(f"{output_dir}/scraped_titles.csv", index=False)
        pd.DataFrame(links, columns=['Links']).to_csv(f"{output_dir}/scraped_links.csv", index=False)
        pd.DataFrame(images, columns=['Images']).to_csv(f"{output_dir}/scraped_images.csv", index=False)

        logging.info(f"Done! Titles: {len(titles)}, Links: {len(links)}, Images: {len(images)}")
        print(f"Saved to {output_dir}/ - Titles: {len(titles)}, Links: {len(links)}, Images: {len(images)}")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed for {url}: {e}")
        return False
    except Exception as e:
        logging.error(f"Scrape error: {e}", exc_info=True)
        return False

def job(url: str):
    scrape_website(url)

def main():
    parser = argparse.ArgumentParser(description="Website scraper with daily schedule")
    parser.add_argument("--url", default="https://example.com", help="URL to scrape")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--time", default="08:00", help="Daily run time HH:MM (24h)")
    args = parser.parse_args()

    # Basic validation
    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        logging.error(f"Invalid URL: {args.url}")
        return

    if args.once or schedule is None:
        if schedule is None and not args.once:
            logging.warning("schedule package not installed (pip install schedule) - running once")
        job(args.url)
    else:
        logging.info(f"Scheduled daily scraping of {args.url} at {args.time}")
        schedule.every().day.at(args.time).do(lambda: job(args.url))
        
        # Run once immediately on start
        job(args.url)
        
        print(f"Scheduler running. Press Ctrl+C to stop.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(30) # check every 30s, not 1s
        except KeyboardInterrupt:
            logging.info("Stopped by user")

if __name__ == "__main__":
    main()
    
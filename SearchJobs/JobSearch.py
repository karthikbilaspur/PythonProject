import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import time
from datetime import datetime

class JobScraper:
    def __init__(self, job_title, location):
        self.job_title = job_title
        self.location = location
        self.job_listings = []

    def scrape_indeed_jobs(self):
        """
        Scrape job listings from Indeed.

        Returns:
            list: List of job listings.
        """
        url = f"https://www.indeed.com/jobs?q={self.job_title}&l={self.location}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        for job in soup.find_all("div", class_="jobsearch-SerpJobCard"):
            title = job.find("h2", class_="title").text.strip()
            company = job.find("span", class_="company").text.strip()
            location = job.find("div", class_="location").text.strip()
            description = job.find("div", class_="summary").text.strip()
            self.job_listings.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Description": description,
                "Source": "Indeed"
            })

    def scrape_linkedin_jobs(self):
        """
        Scrape job listings from LinkedIn.

        Returns:
            list: List of job listings.
        """
        url = f"https://www.linkedin.com/jobs/search/?keywords={self.job_title}&location={self.location}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        for job in soup.find_all("li", class_="jobs-search-results__list-item"):
            title = job.find("h3", class_="base-search-card__title").text.strip()
            company = job.find("h4", class_="base-search-card__subtitle").text.strip()
            location = job.find("span", class_="job-search-card__location").text.strip()
            description = job.find("span", class_="job-card-container__snippet").text.strip()
            self.job_listings.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Description": description,
                "Source": "LinkedIn"
            })

    def scrape_glassdoor_jobs(self):
        """
        Scrape job listings from Glassdoor.

        Returns:
            list: List of job listings.
        """
        url = f"https://www.glassdoor.com/Jobs/{self.job_title}-{self.location}-jobs-SRCH_IL.0,13_IN{self.location}.htm"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        for job in soup.find_all("li", class_="jl"):
            title = job.find("div", class_="title").text.strip()
            company = job.find("div", class_="company").text.strip()
            location = job.find("span", class_="subtle loc").text.strip()
            description = job.find("span", class_="job-description").text.strip()
            self.job_listings.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Description": description,
                "Source": "Glassdoor"
            })

    def save_to_csv(self):
        """
        Save job listings to a CSV file.
        """
        df = pd.DataFrame(self.job_listings)
        df.to_csv(f"{self.job_title}_{self.location}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv", index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Job scraper')
    parser.add_argument('-j', '--job_title', required=True, help='Job title to search for')
    parser.add_argument('-l', '--location', required=True, help='Location to search in')
    parser.add_argument('-s', '--sites', nargs='+', required=True, choices=['indeed', 'linkedin', 'glassdoor'], help='Job boards to scrape')

    args = parser.parse_args()
    scraper = JobScraper(args.job_title, args.location)

    for site in args.sites:
        if site == 'indeed':
            scraper.scrape_indeed_jobs()
        elif site == 'linkedin':
            scraper.scrape_linkedin_jobs()
        elif site == 'glassdoor':
            scraper.scrape_glassdoor_jobs()
        time.sleep(1)  # wait 1 second between requests

    scraper.save_to_csv()
    print(f"Job listings scraped successfully: {len(scraper.job_listings)} jobs found")

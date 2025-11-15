import requests
from bs4 import BeautifulSoup
import itertools
import threading
import time
import sys
import urllib.request
import img2pdf
import os

class SlideshareDownloader:
    def __init__(self, url: str):
        self.url = url
        self.task = False
        self.process = "Getting the slides "
        self.all_slides = []

    def animate(self):
        for i in itertools.cycle(['|', '/', '-', '\\']):
            if self.task:
                break
            sys.stdout.write('\r' + self.process + i)
            sys.stdout.flush()
            time.sleep(0.1)

    def get_image_list(self):
        try:
            code = requests.get(self.url)
            soup = BeautifulSoup(code.text, "html.parser")
            print(f"Title: {soup.title.get_text()}")
            imgs = soup.find_all("img")
            img_urls = [temp_url.get("data-full") for temp_url in imgs if temp_url.get("data-full") is not None]
            return img_urls
        except Exception as e:
            print(f"Error: {e}")
            return []

    def slides_capture(self, links):
        pg_no = 1
        os.makedirs(".cache", exist_ok=True)
        for link in links:
            print(f"Fetching (slide{pg_no})")
            file = f"slide{pg_no}.jpg"
            urllib.request.urlretrieve(link, ".cache/"+file)
            self.all_slides.append(".cache/"+file)
            pg_no += 1

    def combine(self):
        output_name = input("\n\nEnter the name for pdf file of slides (without extension): ")
        try:
            with open(output_name+".pdf", "wb") as f:
                f.write(img2pdf.convert(self.all_slides))
            for i in self.all_slides:
                os.remove(i)
            print("All set, your file is ready")
        except Exception as e:
            print(f"Error: {e}")

    def start(self):
        t = threading.Thread(target=self.animate)
        t.start()
        all_urls = self.get_image_list()
        if len(all_urls) == 0:
            print("Sorry, no downloadable slides found")
            self.task = True
        else:
            print(f"Total number of slides found: {len(all_urls)}")
            self.slides_capture(all_urls)
            self.task = True
            self.combine()

if __name__ == "__main__":
    print("Enter the URL of slides below:")
    main_link = input()
    downloader = SlideshareDownloader(main_link)
    downloader.start()
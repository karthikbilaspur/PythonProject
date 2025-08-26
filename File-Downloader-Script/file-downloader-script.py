import requests
from tqdm import tqdm
import os
from urllib.parse import urlparse
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import concurrent.futures

class AdvancedFileDownloader:
    def __init__(self):
        self.vectorizer = joblib.load('vectorizer.joblib')
        self.model = joblib.load('filename_predictor.joblib')

    def predict_filename(self, url):
        X = self.vectorizer.transform([url])
        filename = self.model.predict(X)[0]
        return filename

    def download_file(self, url, filename=None):
        if not filename:
            filename = self.predict_filename(url)

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        t = tqdm(total=total_size, unit='B', unit_scale=True)

        with open(filename, 'wb') as f:
            for data in response.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()

        if total_size != 0 and t.n != total_size:
            print("Error: Download failed")
        else:
            print("Download complete")

    def download_multiple_files(self, urls):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for url in urls:
                filename = self.predict_filename(url)
                futures.append(executor.submit(self.download_file, url, filename))
            for future in concurrent.futures.as_completed(futures):
                future.result()

def main():
    downloader = AdvancedFileDownloader()
    while True:
        print("1. Download single file")
        print("2. Download multiple files")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            url = input("Enter the URL of the file: ")
            downloader.download_file(url)
        elif choice == "2":
            urls = input("Enter the URLs of the files (separated by commas): ").split(',')
            urls = [url.strip() for url in urls]
            downloader.download_multiple_files(urls)
        elif choice == "3":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
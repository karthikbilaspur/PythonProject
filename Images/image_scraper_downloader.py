import tkinter as tk
from tkinter import ttk
from tkhtmlview import HTMLLabel
import requests
from bs4 import BeautifulSoup
import urllib3
import shutil
from urllib.parse import urljoin, urlparse

class ImageScraperDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer and Downloader")
        self.root.geometry("400x500")

        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.map('my.TButton', background=[('active', 'white')])
        self.style.configure('my.TButton', font=('Helvetica', 16, 'bold'))
        self.style.configure('my.TButton', background='white')
        self.style.configure('my.TButton', foreground='orange')
        self.style.configure('my.TFrame', background='white')

        self.search_box = tk.Entry(self.root, font=("Helvetica 15"), bd=2, width=60)
        self.search_box.pack(side=tk.TOP, pady=5, padx=15, ipadx=5)

        self.search_btn = ttk.Button(self.root, text="Scrape Image!", command=self.show_image, style='my.TButton')
        self.search_btn.pack(side=tk.TOP)

        self.save_btn = ttk.Button(self.root, text="Download Image!", command=self.save_image, style='my.TButton')
        self.save_btn.pack(side=tk.TOP)

        self.my_label = HTMLLabel(self.root)
        self.my_label.pack(pady=20, padx=20)

    def get_image(self):
        search = self.search_box.get()
        url = "https://www.bing.com/images/search?q={}".format(search.replace(' ', '+'))
        try:
            page = requests.get(url)
            page.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

        soup = BeautifulSoup(page.content, 'html.parser')
        images = soup.find_all('img')

        for image in images:
            link = image.get('src')
            if link and link.startswith('http'):
                return link

        return None

    def show_image(self):
        link = self.get_image()
        if link:
            str_value = '<img src="{}">'.format(link)
            self.my_label.set_html(str_value)

    def save_image(self):
        link = self.get_image()
        if link:
            file_name = self.search_box.get().replace(" ", "") + ".jpg"
            http = urllib3.PoolManager()
            try:
                with http.request('GET', link, preload_content=False) as r:
                    with open(file_name, 'wb') as out:
                        shutil.copyfileobj(r, out)
                print(f"Image saved as {file_name}")
            except Exception as e:
                print(f"Failed to save image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageScraperDownloader(root)
    root.mainloop()
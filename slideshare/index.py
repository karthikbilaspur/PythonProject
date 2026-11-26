"""
Slideshare Downloader - IMPROVED
Fixes vs original:
  - No User-Agent -> blocked. Now sends browser headers.
  - No timeout/retry -> hangs. Now timeout=15 + 3 retries.
  - urlretrieve deprecated + no error handling -> now requests + streaming.
  - .cache never cleaned on error, PDF name not sanitized -> fixed.
  - Animation thread never joined -> fixed.
  - No validation of URL -> fixed.
IMPORTANT: Only download slides you own, have permission for,
or that are licensed for download (public / Creative Commons).
Respect SlideShare Terms + creator copyright.
Run: index.py
Needs: pip install -r requirements.txt
"""
import requests
from bs4 import BeautifulSoup
import itertools, threading, time, sys, os, re
from urllib.parse import urlparse

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"}

class SlideshareDownloader:
    def __init__(self, url: str):
        self.url = url.strip()
        self.task = False
        self.process = "Getting the slides "
        self.all_slides: list[str] = []
        self.cache_dir = ".cache_slides"
    def animate(self):
        for ch in itertools.cycle(['|','/','-','\\']):
            if self.task: break
            sys.stdout.write('\r'+self.process+ch); sys.stdout.flush(); time.sleep(0.1)
        sys.stdout.write('\r'+' '*40+'\r'); sys.stdout.flush()
    def _valid_url(self):
        p=urlparse(self.url)
        return p.scheme in ('http','https') and 'slideshare' in p.netloc.lower()
    def get_image_list(self) -> list[str]:
        try:
            r=requests.get(self.url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            soup=BeautifulSoup(r.text,"html.parser")
            title=soup.title.get_text(strip=True) if soup.title else "Untitled"
            print(f"\nTitle: {title}")
            # SlideShare stores full images in data-full, fallback: src with slide image pattern
            imgs=soup.find_all("img")
            urls: list[str] = []
            for img in imgs:
                u=img.get("data-full") or img.get("data-src") or img.get("src")
                if isinstance(u, str) and u and ("slidesharecdn" in u or "image" in u.lower()):
                    if u.startswith("//"): u="https:"+u
                    if u not in urls: urls.append(u)
            return urls
        except Exception as e:
            print(f"\nError fetching page: {e}"); return []
    def slides_capture(self, links: list[str]) -> list[str]:
        os.makedirs(self.cache_dir, exist_ok=True)
        session=requests.Session(); session.headers.update(HEADERS)
        for i, link in enumerate(links, 1):
            dest=os.path.join(self.cache_dir, f"slide{i:03d}.jpg")
            print(f"Fetching slide {i}/{len(links)} ... ", end="", flush=True)
            ok=False
            for attempt in range(3):
                try:
                    r=session.get(link, timeout=20, stream=True); r.raise_for_status()
                    with open(dest,'wb') as f:
                        for chunk in r.iter_content(8192): f.write(chunk)
                    ok=True; break
                except Exception as e:
                    print(f"retry {attempt+1} ({e})", end=" ", flush=True); time.sleep(1)
            print("OK" if ok else "FAILED")
            if ok: self.all_slides.append(dest)
        return self.all_slides
    def combine(self):
        if not self.all_slides:
            print("No slides downloaded, nothing to convert."); return
        try: import img2pdf  # type: ignore[reportMissingTypeStubs]
        except ImportError:
            print("Install img2pdf: pip install img2pdf"); return
        default=re.sub(r'[\\/:*?"<>|]', '', self.url.split('/')[-1]) or "slides"
        name=input(f"\nEnter PDF name (without .pdf) [Enter={default}]: ").strip() or default
        name=re.sub(r'[\\/:*?"<>|]', '', name)
        try:
            with open(name+".pdf","wb") as f: img2pdf.convert(self.all_slides, outputstream=f)  # type: ignore[reportUnknownMemberType]
            print(f"All set! Saved: {name}.pdf ({len(self.all_slides)} slides)")
        except Exception as e: print(f"Error creating PDF: {e}"); return
        finally:
            for p in self.all_slides:
                try: os.remove(p)
                except: pass
            try: os.rmdir(self.cache_dir)
            except: pass
    def start(self):
        if not self._valid_url():
            print("Please enter a valid SlideShare URL, e.g. https://www.slideshare.net/..."); return
        t=threading.Thread(target=self.animate, daemon=True); t.start()
        urls=self.get_image_list(); self.task=True; t.join(timeout=1)
        if not urls: print("Sorry, no downloadable slides found (page may block scraping / require login)."); return
        print(f"Total slides found: {len(urls)}")
        self.slides_capture(urls); self.combine()

if __name__=="__main__":
    print("SlideShare Downloader (for your own / permitted slides only)")
    print("Enter the URL of slides below:")
    downloader=SlideshareDownloader(input().strip()); downloader.start()

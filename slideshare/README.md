# SlideShare Downloader - Improved

index Run
bash
pip install -r requirements.txt
python index.py

Paste SlideShare URL -> enter PDF name

index What Was Fixed

| Original Bug | Fix |
|------|

| No User-Agent -> blocked / empty | Browser headers |
| No timeout -> hangs forever | timeout 15s + 3 retries |
| `urlretrieve` deprecated, no errors | `requests` streaming + retry |
| `.cache` left behind on error | Cleanup in `finally` + numbered files `slide001.jpg` |
| Spinner thread never stopped | `task` flag + `join()` + clear line |
| No URL validation | Checks `slideshare` in domain |
| Duplicate / broken image URLs | Dedupe + fallback `data-src`/`src` |

index ⚠️ Copyright - Read This
Only download slides you **own**, have **permission** for, or that are **public / Creative Commons** licensed for download.
Do not re-upload / sell someone else's deck. If SlideShare shows no download / blocks scraping, that is intentional.

index Requirements
`requests`, `beautifulsoup4`, `img2pdf`

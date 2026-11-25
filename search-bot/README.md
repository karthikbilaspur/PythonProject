# Search Bot

Fetch a web page, summarise it, make a word cloud, save the summary.

## Requirements
```bash
pip install requests beautifulsoup4 wordcloud matplotlib
```

## Run
```bash
python search_bot.py
```

## How to use
1. Paste a full article/page URL (e.g. a Wikipedia article) — default is filled in.
2. Set summary length 0–1 (e.g. 0.1 = ~10% of sentences).
3. Click **Fetch + Summarise**.
4. **Word Cloud** plots the summary, **Save Summary** writes it to `.txt`.

## Fixes vs original version
- `gensim.summarization.summarize` was REMOVED in gensim 4.x and crashed on import — replaced with a small built-in extractive summariser (word-frequency sentence scoring, no gensim needed).
- Original tried to scrape Google/Bing HTML — search engines block that and return junk/ToS issues. This version fetches a URL you paste.
- Added User-Agent header, timeout, and a guard for pages with almost no readable text.

## Limitations
- JS-heavy pages (need a browser to render) will return little text.
- Extractive summary picks existing sentences — it doesn't paraphrase like an LLM.
- Word cloud needs a non-empty summary first.

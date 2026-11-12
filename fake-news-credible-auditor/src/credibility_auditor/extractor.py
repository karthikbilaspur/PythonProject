from __future__ import annotations

import json
from urllib.parse import urljoin, urlparse

import trafilatura
from lxml import html as lxml_html

from .errors import ExtractionError
from .models import Article


def _extract_links(html: str | bytes, base_url: str) -> list[str]:
    try:
        doc = lxml_html.fromstring(html)
    except Exception:
        return []
    seen: dict[str, None] = {}
    for href in doc.xpath("//a/@href"):
        absolute = urljoin(base_url, href.strip())
        if urlparse(absolute).scheme in ("http", "https"):
            seen.setdefault(absolute, None)
    return list(seen)


def extract_article(url: str, html: str | bytes, min_text_chars: int = 200) -> Article:
    """Main text and metadata via trafilatura; links are taken from the full page."""
    raw = trafilatura.extract(html, url=url, output_format="json", with_metadata=True)
    if not raw:
        raise ExtractionError("No article text could be extracted from the page.")
    data = json.loads(raw)
    text = (data.get("text") or "").strip()
    if len(text) < min_text_chars:
        raise ExtractionError(
            f"Extracted only {len(text)} characters (minimum {min_text_chars}); "
            "page may not be an article."
        )
    return Article(
        url=url,
        title=(data.get("title") or "").strip(),
        text=text,
        author=data.get("author"),
        date=data.get("date"),
        links=_extract_links(html, url),
    )

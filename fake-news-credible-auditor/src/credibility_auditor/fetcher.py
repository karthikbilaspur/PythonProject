from __future__ import annotations

from urllib.parse import urlparse

import httpx

from .errors import FetchError

USER_AGENT = "Mozilla/5.0 (compatible; credibility-auditor/0.1)"
_HTML_TYPES = ("text/html", "application/xhtml+xml")


def fetch_html(
    url: str,
    client: httpx.Client | None = None,
    timeout: float = 15,
    max_bytes: int = 5_000_000,
) -> bytes:
    """Download a page and return raw bytes (the extractor handles encoding)."""
    if urlparse(url).scheme not in ("http", "https"):
        raise FetchError(f"Only http(s) URLs are supported: {url}")

    owns_client = client is None
    if client is None:
        client = httpx.Client(
            headers={"User-Agent": USER_AGENT}, timeout=timeout, follow_redirects=True
        )
    try:
        with client.stream("GET", url) as response:
            response.raise_for_status()
            ctype = response.headers.get("content-type", "").split(";")[0].strip().lower()
            if ctype and ctype not in _HTML_TYPES:
                raise FetchError(f"Not an HTML page (content-type: {ctype})")
            body = bytearray()
            for chunk in response.iter_bytes():
                body.extend(chunk)
                if len(body) > max_bytes:
                    raise FetchError(f"Page larger than {max_bytes} bytes")
            return bytes(body)
    except httpx.HTTPStatusError as exc:
        raise FetchError(f"HTTP {exc.response.status_code} for {url}") from exc
    except httpx.HTTPError as exc:
        raise FetchError(f"Request failed for {url}: {exc}") from exc
    finally:
        if owns_client:
            client.close()

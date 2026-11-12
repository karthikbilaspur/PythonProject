from __future__ import annotations

import tldextract

# suffix_list_urls=() -> use the bundled public-suffix snapshot, no network call.
_extract = tldextract.TLDExtract(suffix_list_urls=(), cache_dir=None)


def registered_domain(url_or_host: str) -> str:
    """'https://news.bbc.co.uk/x' -> 'bbc.co.uk'. Returns '' if unparseable."""
    try:
        parts = _extract(url_or_host)
    except Exception:
        return ""
    if parts.suffix:
        return f"{parts.domain}.{parts.suffix}".lower()
    return parts.domain.lower()

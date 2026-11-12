import httpx
import pytest

from credibility_auditor.errors import FetchError
from credibility_auditor.fetcher import fetch_html


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_returns_html_bytes():
    client = _client(lambda r: httpx.Response(200, headers={"content-type": "text/html; charset=utf-8"}, content=b"<p>ok</p>"))
    assert fetch_html("https://example.org", client=client) == b"<p>ok</p>"


def test_http_error_becomes_fetch_error():
    client = _client(lambda r: httpx.Response(404, headers={"content-type": "text/html"}))
    with pytest.raises(FetchError, match="404"):
        fetch_html("https://example.org", client=client)


def test_non_html_rejected():
    client = _client(lambda r: httpx.Response(200, headers={"content-type": "application/pdf"}, content=b"%PDF"))
    with pytest.raises(FetchError, match="Not an HTML"):
        fetch_html("https://example.org/file.pdf", client=client)


def test_size_limit():
    client = _client(lambda r: httpx.Response(200, headers={"content-type": "text/html"}, content=b"x" * 1000))
    with pytest.raises(FetchError, match="larger"):
        fetch_html("https://example.org", client=client, max_bytes=100)


def test_non_http_scheme_rejected():
    with pytest.raises(FetchError):
        fetch_html("file:///etc/passwd")

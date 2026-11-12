import pytest

from credibility_auditor.errors import ExtractionError
from credibility_auditor.extractor import extract_article


def test_extracts_text_and_metadata(sample_html):
    article = extract_article("https://news.example.org/budget", sample_html)
    assert "transit budget" in article.text
    assert article.title
    assert len(article.text) > 200


def test_links_come_from_whole_page_and_are_absolute(sample_html):
    article = extract_article("https://news.example.org/budget", sample_html)
    assert "https://www.reuters.com/world/example-story" in article.links
    assert "https://news.example.org/budget" in article.links  # relative /budget resolved
    # footer link is kept (citations should not be lost with boilerplate removal)
    assert "https://www.infowars.com/some-page" in article.links


def test_rejects_pages_without_article_text():
    with pytest.raises(ExtractionError):
        extract_article("https://example.org", "<html><body><p>Hi</p></body></html>")

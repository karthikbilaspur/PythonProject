from pathlib import Path

import pytest

from credibility_auditor.models import Article

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_html() -> str:
    return (FIXTURES / "sample_article.html").read_text(encoding="utf-8")


@pytest.fixture
def make_article():
    def _make(url="https://example.org/story", links=None, text="word " * 100, title="Title"):
        return Article(url=url, title=title, text=text, links=links or [])

    return _make

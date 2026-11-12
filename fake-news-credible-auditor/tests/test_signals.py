from credibility_auditor.signals import CitationSignal, ContentModelSignal, SourceReputationSignal
from credibility_auditor.signals.content_model import chunk_words

TRUSTED = ["reuters.com", "bbc.co.uk"]
SUSPICIOUS = ["infowars.com"]


def test_source_trusted_uses_registered_domain(make_article):
    result = SourceReputationSignal(TRUSTED, SUSPICIOUS).evaluate(make_article("https://news.bbc.co.uk/a"))
    assert result.score == 0.9


def test_source_suspicious(make_article):
    result = SourceReputationSignal(TRUSTED, SUSPICIOUS).evaluate(make_article("https://www.infowars.com/x"))
    assert result.score == 0.1


def test_source_lookalike_domain_is_not_trusted(make_article):
    # substring matching would have trusted this; domain matching must not
    result = SourceReputationSignal(TRUSTED, SUSPICIOUS).evaluate(make_article("https://reuters.com.evil.example/a"))
    assert result.score is None


def test_citations_bonus_is_capped_and_unique(make_article):
    links = [f"https://www.reuters.com/p{i}" for i in range(20)] + ["https://www.bbc.co.uk/x"]
    result = CitationSignal(TRUSTED, SUSPICIOUS).evaluate(make_article(links=links))
    assert result.score == 0.5 + 0.2  # two unique trusted domains, not 21 links


def test_citations_suspicious_penalty(make_article):
    result = CitationSignal(TRUSTED, SUSPICIOUS).evaluate(make_article(links=["https://infowars.com/a"]))
    assert result.score < 0.5


def test_citations_ignore_own_domain(make_article):
    result = CitationSignal(["example.org"], []).evaluate(
        make_article("https://example.org/a", links=["https://www.example.org/b"])
    )
    assert result.score is None


def test_chunking_overlaps_and_caps():
    text = " ".join(str(i) for i in range(1000))
    chunks = chunk_words(text, size=300, overlap=50, max_chunks=3)
    assert len(chunks) == 3
    assert chunks[0].split()[-50:] == chunks[1].split()[:50]


def test_content_model_maps_labels_and_caps_confidence(make_article):
    fake = lambda chunks: [{"label": "LABEL_1", "score": 1.0} for _ in chunks]
    signal = ContentModelSignal("x", ["LABEL_1"], max_confidence=0.6, classifier=fake)
    result = signal.evaluate(make_article())
    assert result.score == 1.0
    assert result.confidence == 0.6


def test_content_model_inverts_when_label_is_fake(make_article):
    fake = lambda chunks: [{"label": "LABEL_0", "score": 0.9} for _ in chunks]
    result = ContentModelSignal("x", ["LABEL_1"], classifier=fake).evaluate(make_article())
    assert abs(result.score - 0.1) < 1e-9


def test_content_model_failure_abstains(make_article):
    def boom(chunks):
        raise RuntimeError("no weights")

    result = ContentModelSignal("x", ["LABEL_1"], classifier=boom).evaluate(make_article())
    assert result.score is None

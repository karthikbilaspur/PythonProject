import pytest

from credibility_auditor.config import load_config
from credibility_auditor.errors import ExtractionError
from credibility_auditor.evaluate import evaluate
from credibility_auditor.pipeline import build_pipeline
from credibility_auditor.signals import ContentModelSignal


def _pipeline(sample_html, label="LABEL_1", score=0.95, use_model=True):
    pipeline = build_pipeline(load_config(), use_model=use_model, fetcher=lambda url: sample_html.encode())
    for i, s in enumerate(pipeline.signals):
        if isinstance(s, ContentModelSignal):
            s._classifier = lambda chunks: [{"label": label, "score": score} for _ in chunks]
    return pipeline


def test_end_to_end_credible(sample_html):
    report = _pipeline(sample_html).audit("https://www.bbc.com/news/budget")
    assert report.verdict == "LIKELY_CREDIBLE"
    assert {s.name for s in report.signals} == {"source", "citations", "content_model"}


def test_suspicious_source_scores_low(sample_html):
    report = _pipeline(sample_html, label="LABEL_0").audit("https://www.infowars.com/story")
    assert report.verdict == "LIKELY_UNRELIABLE"


def test_unknown_source_without_model_has_insufficient_evidence(sample_html):
    report = _pipeline(sample_html, use_model=False).audit("https://unknown-site.example/story")
    # citations signal sees trusted + suspicious links and nets out near the middle,
    # but with a small evidence weight; either way a verdict is produced without crashing
    assert report.verdict in {"INSUFFICIENT_EVIDENCE", "QUESTIONABLE"}


def test_report_is_json_serializable(sample_html):
    import json

    report = _pipeline(sample_html).audit("https://www.bbc.com/news/budget")
    json.dumps(report.to_dict())


def test_bad_page_raises_extraction_error():
    pipeline = build_pipeline(load_config(), use_model=False, fetcher=lambda url: b"<html><body>tiny</body></html>")
    with pytest.raises(ExtractionError):
        pipeline.audit("https://example.org")


def test_evaluate_counts(sample_html, tmp_path):
    csv_file = tmp_path / "labels.csv"
    csv_file.write_text(
        "url,label\nhttps://www.bbc.com/a,credible\nhttps://www.infowars.com/b,unreliable\n"
    )
    stats = evaluate(csv_file, _pipeline(sample_html))
    assert stats["total"] == 2
    assert stats["errors"] == 0

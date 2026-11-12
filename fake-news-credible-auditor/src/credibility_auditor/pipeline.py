from __future__ import annotations

from typing import Callable

from .extractor import extract_article
from .fetcher import fetch_html
from .models import Report
from .scoring import combine
from .signals import CitationSignal, ContentModelSignal, Signal, SourceReputationSignal

Fetcher = Callable[[str], bytes]


class Pipeline:
    """fetch -> extract -> signals -> score."""

    def __init__(
        self,
        signals: list[Signal],
        weights: dict[str, float],
        scoring: dict,
        min_text_chars: int = 200,
        fetcher: Fetcher = fetch_html,
    ):
        self.signals = signals
        self.weights = weights
        self.scoring = scoring
        self.min_text_chars = min_text_chars
        self.fetcher = fetcher

    def audit(self, url: str, html: str | bytes | None = None) -> Report:
        page = html if html is not None else self.fetcher(url)
        article = extract_article(url, page, self.min_text_chars)
        results = [signal.evaluate(article) for signal in self.signals]
        score, verdict, weight = combine(
            results,
            self.weights,
            self.scoring["min_evidence"],
            self.scoring["unreliable_below"],
            self.scoring["questionable_below"],
        )
        return Report(url, article.title, score, verdict, weight, results)


def build_pipeline(cfg: dict, use_model: bool = True, fetcher: Fetcher | None = None) -> Pipeline:
    trusted = cfg["domains"]["trusted"]
    suspicious = cfg["domains"]["suspicious"]
    signals: list[Signal] = [
        SourceReputationSignal(trusted, suspicious),
        CitationSignal(trusted, suspicious),
    ]
    if use_model:
        m = cfg["model"]
        signals.append(
            ContentModelSignal(
                m["name"], m["real_labels"], m["max_confidence"],
                m["chunk_words"], m["overlap_words"], m["max_chunks"],
            )
        )
    if fetcher is None:
        fetch_cfg = cfg["fetch"]
        fetcher = lambda url: fetch_html(url, timeout=fetch_cfg["timeout"], max_bytes=fetch_cfg["max_bytes"])
    return Pipeline(
        signals, cfg["weights"], cfg["scoring"], cfg["extraction"]["min_text_chars"], fetcher
    )

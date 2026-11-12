from __future__ import annotations

import logging
from typing import Callable

from ..models import Article, SignalResult

log = logging.getLogger(__name__)

Classifier = Callable[[list[str]], list[dict]]


def chunk_words(text: str, size: int = 300, overlap: int = 50, max_chunks: int = 8) -> list[str]:
    """Split text into overlapping word windows so long articles are not just truncated."""
    words = text.split()
    if not words:
        return []
    step = max(1, size - overlap)
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start : start + size]))
        if start + size >= len(words) or len(chunks) >= max_chunks:
            break
    return chunks


class ContentModelSignal:
    """Transformer text classifier, applied per chunk and averaged.

    Treated as weak evidence: its confidence is capped by `max_confidence`.
    Pass `classifier` (a callable taking a list of strings and returning
    [{'label':..., 'score':...}, ...]) to avoid loading a real model, e.g. in tests.
    """

    name = "content_model"

    def __init__(
        self,
        model_name: str,
        real_labels: list[str],
        max_confidence: float = 0.6,
        chunk_size: int = 300,
        overlap: int = 50,
        max_chunks: int = 8,
        classifier: Classifier | None = None,
    ):
        self.model_name = model_name
        self.real_labels = set(real_labels)
        self.max_confidence = max_confidence
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.max_chunks = max_chunks
        self._classifier = classifier

    def _get_classifier(self) -> Classifier:
        if self._classifier is None:
            try:
                from transformers import pipeline
            except ImportError as exc:
                raise RuntimeError(
                    "The content model needs transformers and torch: pip install '.[model]'"
                ) from exc
            log.info("Loading model %s (first run downloads weights)", self.model_name)
            pipe = pipeline("text-classification", model=self.model_name)
            self._classifier = lambda chunks: pipe(chunks, truncation=True, max_length=512)
        return self._classifier

    def evaluate(self, article: Article) -> SignalResult:
        chunks = chunk_words(
            f"{article.title}. {article.text}", self.chunk_size, self.overlap, self.max_chunks
        )
        if not chunks:
            return SignalResult.abstain(self.name, "No text to classify")
        try:
            outputs = self._get_classifier()(chunks)
        except Exception as exc:  # model failures must not kill the whole audit
            log.warning("Content model failed: %s", exc)
            return SignalResult.abstain(self.name, f"Model unavailable: {exc}")

        real_probs = [
            o["score"] if o["label"] in self.real_labels else 1.0 - o["score"] for o in outputs
        ]
        mean_real = sum(real_probs) / len(real_probs)
        confidence = min(abs(mean_real - 0.5) * 2, 1.0) * self.max_confidence
        evidence = [
            f"Model '{self.model_name}' rated {len(chunks)} chunk(s); mean real-news probability {mean_real:.2f}"
        ]
        return SignalResult(self.name, mean_real, confidence, evidence)

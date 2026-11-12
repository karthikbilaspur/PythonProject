from __future__ import annotations

from typing import Protocol

from ..models import Article, SignalResult


class Signal(Protocol):
    """Anything with a name and an evaluate() method can join the pipeline."""

    name: str

    def evaluate(self, article: Article) -> SignalResult: ...

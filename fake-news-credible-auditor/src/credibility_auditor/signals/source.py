from __future__ import annotations

from ..domains import registered_domain
from ..models import Article, SignalResult


class SourceReputationSignal:
    name = "source"

    def __init__(self, trusted: list[str], suspicious: list[str]):
        self.trusted = {d.lower() for d in trusted}
        self.suspicious = {d.lower() for d in suspicious}

    def evaluate(self, article: Article) -> SignalResult:
        domain = registered_domain(article.url)
        if domain in self.trusted:
            return SignalResult(self.name, 0.9, 0.8, [f"{domain} is on the trusted source list"])
        if domain in self.suspicious:
            return SignalResult(self.name, 0.1, 0.9, [f"{domain} is on the suspicious source list"])
        return SignalResult.abstain(self.name, f"{domain or 'unknown domain'} is not in the reputation lists")

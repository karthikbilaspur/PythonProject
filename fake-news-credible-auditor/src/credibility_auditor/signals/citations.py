from __future__ import annotations

from ..domains import registered_domain
from ..models import Article, SignalResult


class CitationSignal:
    """Looks at which *unique* external domains the article links to.

    Counting unique domains (with a cap) stops one outlet from being linked
    repeatedly to inflate the score.
    """

    name = "citations"

    def __init__(self, trusted: list[str], suspicious: list[str]):
        self.trusted = {d.lower() for d in trusted}
        self.suspicious = {d.lower() for d in suspicious}

    def evaluate(self, article: Article) -> SignalResult:
        own = registered_domain(article.url)
        domains = {registered_domain(link) for link in article.links} - {own, ""}
        trusted = sorted(domains & self.trusted)
        suspicious = sorted(domains & self.suspicious)

        if not trusted and not suspicious:
            return SignalResult.abstain(
                self.name, f"{len(domains)} external domains linked, none in the reputation lists"
            )

        score = 0.5 + min(0.1 * len(trusted), 0.3) - min(0.2 * len(suspicious), 0.4)
        score = max(0.0, min(1.0, score))
        evidence = []
        if trusted:
            evidence.append("Links to trusted domains: " + ", ".join(trusted))
        if suspicious:
            evidence.append("Links to suspicious domains: " + ", ".join(suspicious))
        return SignalResult(self.name, score, 0.3, evidence)

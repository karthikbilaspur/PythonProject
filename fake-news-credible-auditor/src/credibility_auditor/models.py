from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Article:
    url: str
    title: str
    text: str
    author: str | None = None
    date: str | None = None
    links: list[str] = field(default_factory=list)


@dataclass
class SignalResult:
    """One signal's opinion. score is credibility in [0, 1]; None means 'abstain'."""

    name: str
    score: float | None
    confidence: float
    evidence: list[str] = field(default_factory=list)

    @classmethod
    def abstain(cls, name: str, reason: str) -> "SignalResult":
        return cls(name=name, score=None, confidence=0.0, evidence=[reason])


@dataclass
class Report:
    url: str
    title: str
    score: float | None
    verdict: str
    evidence_weight: float
    signals: list[SignalResult]

    def to_dict(self) -> dict:
        return asdict(self)

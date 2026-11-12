from credibility_auditor.models import SignalResult
from credibility_auditor.scoring import CREDIBLE, INSUFFICIENT, QUESTIONABLE, UNRELIABLE, combine

KW = dict(weights={"a": 1.0, "b": 2.0}, min_evidence=0.3, unreliable_below=0.4, questionable_below=0.7)


def test_weighted_mean():
    results = [SignalResult("a", 1.0, 1.0), SignalResult("b", 0.0, 1.0)]
    score, verdict, weight = combine(results, **KW)
    assert abs(score - 1 / 3) < 1e-9
    assert verdict == UNRELIABLE
    assert weight == 3.0


def test_abstentions_are_ignored():
    results = [SignalResult("a", 0.9, 1.0), SignalResult.abstain("b", "n/a")]
    score, verdict, _ = combine(results, **KW)
    assert score == 0.9 and verdict == CREDIBLE


def test_insufficient_evidence_gives_no_score():
    score, verdict, _ = combine([SignalResult("a", 0.9, 0.1)], **KW)
    assert score is None and verdict == INSUFFICIENT


def test_questionable_band():
    score, verdict, _ = combine([SignalResult("a", 0.55, 1.0)], **KW)
    assert verdict == QUESTIONABLE


def test_all_abstain():
    _, verdict, weight = combine([SignalResult.abstain("a", "x")], **KW)
    assert verdict == INSUFFICIENT and weight == 0

from __future__ import annotations

from .models import SignalResult

INSUFFICIENT = "INSUFFICIENT_EVIDENCE"
UNRELIABLE = "LIKELY_UNRELIABLE"
QUESTIONABLE = "QUESTIONABLE"
CREDIBLE = "LIKELY_CREDIBLE"


def combine(
    results: list[SignalResult],
    weights: dict[str, float],
    min_evidence: float,
    unreliable_below: float,
    questionable_below: float,
) -> tuple[float | None, str, float]:
    """Confidence-weighted mean of non-abstaining signals.

    Returns (score, verdict, evidence_weight). If the total evidence weight is
    below `min_evidence`, no score is produced rather than forcing a verdict.
    """
    numerator = denominator = 0.0
    for result in results:
        if result.score is None:
            continue
        w = weights.get(result.name, 1.0) * result.confidence
        numerator += w * result.score
        denominator += w

    if denominator < min_evidence or denominator == 0:
        return None, INSUFFICIENT, denominator

    score = numerator / denominator
    if score < unreliable_below:
        verdict = UNRELIABLE
    elif score < questionable_below:
        verdict = QUESTIONABLE
    else:
        verdict = CREDIBLE
    return score, verdict, denominator

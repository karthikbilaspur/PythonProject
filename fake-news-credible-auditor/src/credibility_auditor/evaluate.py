from __future__ import annotations

import csv
from pathlib import Path

from .errors import AuditError
from .pipeline import Pipeline
from .scoring import CREDIBLE, UNRELIABLE


def evaluate(csv_path: str | Path, pipeline: Pipeline) -> dict:
    """Compare verdicts to labels ('credible' / 'unreliable') from a CSV with url,label.

    QUESTIONABLE and INSUFFICIENT_EVIDENCE count as abstentions, so accuracy is
    reported together with coverage.
    """
    stats = {"total": 0, "errors": 0, "abstained": 0, "correct": 0, "wrong": 0}
    with open(csv_path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            url, label = (row.get("url") or "").strip(), (row.get("label") or "").strip().lower()
            if not url or label not in ("credible", "unreliable"):
                continue
            stats["total"] += 1
            try:
                verdict = pipeline.audit(url).verdict
            except AuditError:
                stats["errors"] += 1
                continue
            predicted = {CREDIBLE: "credible", UNRELIABLE: "unreliable"}.get(verdict)
            if predicted is None:
                stats["abstained"] += 1
            elif predicted == label:
                stats["correct"] += 1
            else:
                stats["wrong"] += 1
    decided = stats["correct"] + stats["wrong"]
    scored = stats["total"] - stats["errors"]
    stats["accuracy"] = stats["correct"] / decided if decided else None
    stats["coverage"] = decided / scored if scored else None
    return stats

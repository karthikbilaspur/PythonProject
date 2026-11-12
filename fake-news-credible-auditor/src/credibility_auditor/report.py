from __future__ import annotations

import json

from rich.console import Console
from rich.table import Table

from .models import Report
from .scoring import CREDIBLE, INSUFFICIENT, QUESTIONABLE, UNRELIABLE

_COLORS = {CREDIBLE: "green", QUESTIONABLE: "yellow", UNRELIABLE: "red", INSUFFICIENT: "cyan"}


def to_json(report: Report, indent: int | None = 2) -> str:
    return json.dumps(report.to_dict(), indent=indent, ensure_ascii=False)


def render_terminal(report: Report, console: Console | None = None) -> None:
    console = console or Console()
    color = _COLORS.get(report.verdict, "white")
    console.print(f"[bold]{report.title or report.url}[/bold]")
    console.print(report.url, style="dim")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Signal")
    table.add_column("Score", justify="right")
    table.add_column("Confidence", justify="right")
    table.add_column("Evidence")
    for s in report.signals:
        score = "abstain" if s.score is None else f"{s.score:.0%}"
        table.add_row(s.name, score, f"{s.confidence:.2f}", "\n".join(s.evidence))
    console.print(table)

    if report.score is None:
        console.print(f"[{color}]Verdict: {report.verdict}[/{color}] (evidence weight {report.evidence_weight:.2f})")
    else:
        console.print(f"[{color}]Verdict: {report.verdict}[/{color}] - credibility {report.score:.0%}")
    console.print("Heuristic estimate, not a fact-check. Verify important claims manually.", style="dim")

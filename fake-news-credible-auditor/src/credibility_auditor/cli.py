from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .config import load_config
from .errors import AuditError
from .evaluate import evaluate as run_evaluation
from .pipeline import build_pipeline
from .report import render_terminal, to_json

app = typer.Typer(add_completion=False, help="Multi-signal credibility scoring for news articles.")
err = Console(stderr=True)

ConfigOpt = typer.Option(None, "--config", "-c", help="YAML config overriding the defaults.")
NoModelOpt = typer.Option(False, "--no-model", help="Skip the transformer signal (fast, no downloads).")


def _setup(verbose: bool) -> None:
    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING, format="%(levelname)s %(message)s")


@app.command()
def audit(
    url: str,
    config: Optional[Path] = ConfigOpt,
    as_json: bool = typer.Option(False, "--json", help="Print the report as JSON."),
    no_model: bool = NoModelOpt,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Audit a single article URL."""
    _setup(verbose)
    pipeline = build_pipeline(load_config(config), use_model=not no_model)
    try:
        report = pipeline.audit(url)
    except AuditError as exc:
        err.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)
    if as_json:
        typer.echo(to_json(report))
    else:
        render_terminal(report)


@app.command()
def batch(
    urls_file: Path = typer.Argument(..., exists=True, help="Text file, one URL per line."),
    out: Optional[Path] = typer.Option(None, "--out", "-o", help="Write JSON Lines here (default: stdout)."),
    config: Optional[Path] = ConfigOpt,
    no_model: bool = NoModelOpt,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Audit many URLs and emit one JSON object per line."""
    import json

    _setup(verbose)
    pipeline = build_pipeline(load_config(config), use_model=not no_model)
    urls = [u.strip() for u in urls_file.read_text(encoding="utf-8").splitlines() if u.strip() and not u.startswith("#")]
    lines = []
    for url in urls:
        try:
            lines.append(to_json(pipeline.audit(url), indent=None))
        except AuditError as exc:
            lines.append(json.dumps({"url": url, "error": str(exc)}))
    payload = "\n".join(lines)
    if out:
        out.write_text(payload + "\n", encoding="utf-8")
        err.print(f"Wrote {len(lines)} result(s) to {out}")
    else:
        typer.echo(payload)


@app.command()
def evaluate(
    labeled_csv: Path = typer.Argument(Path("data/labeled_urls.csv"), exists=True),
    config: Optional[Path] = ConfigOpt,
    no_model: bool = NoModelOpt,
) -> None:
    """Score a labeled CSV (url,label) and print accuracy and coverage."""
    pipeline = build_pipeline(load_config(config), use_model=not no_model)
    for key, value in run_evaluation(labeled_csv, pipeline).items():
        typer.echo(f"{key}: {value if not isinstance(value, float) else f'{value:.2%}'}")


if __name__ == "__main__":
    app()

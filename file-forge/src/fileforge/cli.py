from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import BarColumn, DownloadColumn, Progress, TextColumn, TransferSpeedColumn
from rich.table import Table

from . import carve as carve_mod
from . import integrity as integrity_mod
from . import journal as journal_mod
from .dedupe import find_duplicates, quarantine
from .errors import FileForgeError
from .fetch import download
from .organize import DEFAULT_RULES, load_rules, plan_organize
from .search import HashingEmbedder, Index, SentenceTransformerEmbedder
from .util import fileforge_home, human_size
from .vault import SUFFIX, decrypt_file, encrypt_file, password_issues
from .watch import WatchHandler, run_watch

app = typer.Typer(add_completion=False, no_args_is_help=True, help="FileForge: a safe-by-default file toolkit.")
vault_app = typer.Typer(no_args_is_help=True, help="Password-based file encryption (scrypt + AES-256-GCM).")
search_app = typer.Typer(no_args_is_help=True, help="Search file contents (BM25 + optional embeddings).")
integrity_app = typer.Typer(no_args_is_help=True, help="Hash baselines: detect added, removed, modified files.")
app.add_typer(vault_app, name="vault")
app.add_typer(search_app, name="search")
app.add_typer(integrity_app, name="integrity")

console = Console()
err = Console(stderr=True)


@contextmanager
def guard():
    try:
        yield
    except FileForgeError as exc:
        err.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)


def _require_dir(path: Path) -> None:
    if not path.is_dir():
        err.print(f"[red]Error:[/red] not a directory: {path}")
        raise typer.Exit(1)


# --------------------------------------------------------------------------- organize / undo
@app.command()
def organize(
    directory: Path,
    rules: Optional[Path] = typer.Option(None, "--rules", help="YAML: category -> [extensions]."),
    recursive: bool = typer.Option(False, "--recursive", "-r"),
    by_date: bool = typer.Option(False, "--by-date", help="Add a YYYY-MM subfolder (by modified time)."),
    apply: bool = typer.Option(False, "--apply", help="Actually move files. Without it this is a dry run."),
) -> None:
    """Sort files into category folders. Dry run by default; every applied run can be undone."""
    _require_dir(directory)
    with guard():
        moves = plan_organize(directory, load_rules(rules) if rules else DEFAULT_RULES, recursive, by_date)
        if not moves:
            console.print("Nothing to organize.")
            return
        table = Table("From", "To")
        for m in moves:
            table.add_row(str(m.src.relative_to(directory)), str(m.dst.relative_to(directory)))
        console.print(table)
        if not apply:
            console.print(f"[yellow]Dry run:[/yellow] {len(moves)} file(s) would move. Re-run with --apply.")
            return
        done, journal = journal_mod.apply_moves(moves, "organize")
        console.print(f"[green]Moved {len(done)} file(s).[/green] Undo with: fileforge undo {journal}")


@app.command()
def undo(
    journal: Optional[Path] = typer.Argument(None, help="Journal file (default: the latest not yet undone)."),
    list_only: bool = typer.Option(False, "--list", help="List journals instead of undoing."),
) -> None:
    """Reverse a previous organize / dedupe / watch run."""
    with guard():
        if list_only:
            for path in journal_mod.list_journals():
                console.print(path)
            return
        target = journal or journal_mod.latest_journal()
        if target is None:
            console.print("No journals to undo.")
            return
        restored, skipped = journal_mod.undo(target)
        console.print(f"[green]Restored {len(restored)} file(s).[/green]")
        for move, reason in skipped:
            console.print(f"[yellow]Skipped[/yellow] {move.dst}: {reason}")


# --------------------------------------------------------------------------- dedupe
@app.command()
def dedupe(
    directory: Path,
    min_size: int = typer.Option(1, "--min-size", help="Ignore files smaller than this many bytes."),
    quarantine_dir: Optional[Path] = typer.Option(None, "--quarantine", help="Move duplicates here (nothing is deleted)."),
) -> None:
    """Find exact duplicate files (size, then partial hash, then full hash)."""
    _require_dir(directory)
    with guard():
        groups = find_duplicates(directory, min_size)
        if not groups:
            console.print("No duplicates found.")
            return
        for g in groups:
            console.print(f"[bold]{human_size(g.size)} x {len(g.files)}[/bold]  keep: {g.files[0]}")
            for dup in g.files[1:]:
                console.print(f"    duplicate: {dup}")
        console.print(f"Reclaimable space: [bold]{human_size(sum(g.wasted for g in groups))}[/bold]")
        if quarantine_dir:
            done, journal = quarantine(groups, quarantine_dir)
            console.print(f"[green]Moved {len(done)} duplicate(s).[/green] Undo with: fileforge undo {journal}")


# --------------------------------------------------------------------------- vault
@vault_app.command("encrypt")
def vault_encrypt(
    file: Path,
    out: Optional[Path] = typer.Option(None, "--out", "-o"),
    remove_original: bool = typer.Option(False, "--remove-original", help="Delete the plaintext afterwards (not a secure erase)."),
    allow_weak: bool = typer.Option(False, "--allow-weak", help="Accept a password that fails the strength check."),
) -> None:
    """Encrypt FILE to FILE.ffv. The original is kept unless --remove-original."""
    with guard():
        password = typer.prompt("Password", hide_input=True, confirmation_prompt=True)
        issues = password_issues(password)
        if issues and not allow_weak:
            err.print("[red]Weak password:[/red] " + "; ".join(issues) + " (use --allow-weak to override)")
            raise typer.Exit(1)
        result = encrypt_file(file, password, out)
        console.print(f"[green]Encrypted[/green] -> {result}")
        if remove_original:
            file.unlink()
            console.print(f"Removed {file}")


@vault_app.command("decrypt")
def vault_decrypt(file: Path, out: Optional[Path] = typer.Option(None, "--out", "-o")) -> None:
    """Decrypt a .ffv file. Fails cleanly on a wrong password or tampering."""
    with guard():
        password = typer.prompt("Password", hide_input=True)
        console.print(f"[green]Decrypted[/green] -> {decrypt_file(file, password, out)}")


# --------------------------------------------------------------------------- carve
@app.command()
def carve(
    source: Path = typer.Argument(..., exists=True, help="A file, disk image, or directory."),
    out: Path = typer.Option(Path("carved"), "--out", "-o"),
    kinds: Optional[str] = typer.Option(None, "--kinds", help=f"Comma list from: {', '.join(carve_mod.SIGNATURES)}"),
    keep_invalid: bool = typer.Option(False, "--keep-invalid", help="Also keep candidates that fail validation."),
) -> None:
    """Recover embedded JPEG/PNG/PDF/ZIP files and write report.json + report.csv."""
    try:
        results, rejected = carve_mod.carve(source, out, kinds.split(",") if kinds else None, keep_invalid)
    except ValueError as exc:
        err.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)
    json_path, csv_path = carve_mod.write_report(results, out)
    table = Table("#", "Type", "Offset", "Size", "Valid", "SHA-256")
    for i, r in enumerate(results, 1):
        table.add_row(str(i), r.kind, hex(r.offset), human_size(r.length), r.valid, r.sha256[:16] + "...")
    console.print(table)
    console.print(f"Carved {len(results)} file(s), rejected {rejected} invalid candidate(s). Reports: {json_path}, {csv_path}")


# --------------------------------------------------------------------------- search
def _db(db: Optional[Path]) -> Path:
    return db or fileforge_home() / "index.db"


@search_app.command("index")
def search_index(
    directory: Path,
    db: Optional[Path] = typer.Option(None, "--db"),
    bm25_only: bool = typer.Option(False, "--bm25-only", help="Keyword search only (no model download)."),
    model: str = typer.Option("all-MiniLM-L6-v2", "--model"),
    hashing: bool = typer.Option(False, "--hashing", hidden=True, help="Offline stand-in embedder (demos/tests)."),
) -> None:
    """Index (or incrementally update) the text of files under DIRECTORY."""
    _require_dir(directory)
    embedder = None if bm25_only else (HashingEmbedder() if hashing else SentenceTransformerEmbedder(model))
    try:
        index = Index(_db(db), embedder)
        stats = index.update(directory)
        index.close()
    except RuntimeError as exc:
        err.print(f"[red]Error:[/red] {exc} (or use --bm25-only)")
        raise typer.Exit(1)
    console.print(", ".join(f"{k}: {v}" for k, v in stats.items()))


@search_app.command("query")
def search_query(
    text: str,
    db: Optional[Path] = typer.Option(None, "--db"),
    top_k: int = typer.Option(5, "--top", "-k"),
    bm25_only: bool = typer.Option(False, "--bm25-only"),
) -> None:
    """Search the index."""
    path = _db(db)
    if not path.exists():
        err.print("[red]Error:[/red] no index yet. Run: fileforge search index DIR")
        raise typer.Exit(1)
    probe = Index(path)
    stored = probe.stored_embedder()
    probe.close()
    embedder = None
    if stored and not bm25_only:
        embedder = HashingEmbedder() if stored.startswith("hashing-") else SentenceTransformerEmbedder(stored)
    index = Index(path, embedder)
    hits = index.search(text, top_k)
    index.close()
    if not hits:
        console.print("No matches.")
    for hit in hits:
        console.print(f"[bold]{hit.path}[/bold]  [dim](chunk {hit.chunk}, score {hit.score:.4f})[/dim]\n    {hit.snippet}\n")


# --------------------------------------------------------------------------- fetch
@app.command()
def fetch(
    urls: list[str],
    dest: Path = typer.Option(Path("."), "--dest", "-d"),
    sha256: Optional[str] = typer.Option(None, "--sha256", help="Expected checksum (single URL only)."),
    jobs: int = typer.Option(3, "--jobs", "-j", min=1),
) -> None:
    """Download files with resume (.part), retries and optional checksum verification."""
    if sha256 and len(urls) != 1:
        err.print("[red]Error:[/red] --sha256 needs exactly one URL")
        raise typer.Exit(1)
    failures = 0
    with Progress(TextColumn("{task.description}"), BarColumn(), DownloadColumn(), TransferSpeedColumn(), console=console) as progress:
        def work(url: str):
            task = progress.add_task(url[-40:], total=None)
            def on_progress(done: int, total: int | None) -> None:
                progress.update(task, completed=done, total=total)
            return download(url, dest, sha256=sha256, progress=on_progress)

        with ThreadPoolExecutor(max_workers=jobs) as pool:
            futures = {url: pool.submit(work, url) for url in urls}
    for url, future in futures.items():
        try:
            console.print(f"[green]Saved[/green] {future.result()}")
        except FileForgeError as exc:
            failures += 1
            err.print(f"[red]Failed[/red] {url}: {exc}")
    if failures:
        raise typer.Exit(1)


# --------------------------------------------------------------------------- watch
@app.command()
def watch(
    directory: Path,
    auto_organize: bool = typer.Option(False, "--auto-organize", help="Organize new top-level files once they finish writing."),
    rules: Optional[Path] = typer.Option(None, "--rules"),
    recursive: bool = typer.Option(True, "--recursive/--no-recursive"),
) -> None:
    """Log file events live; optionally keep a folder (e.g. Downloads) tidy. Ctrl+C to stop."""
    _require_dir(directory)
    with guard():
        handler = WatchHandler(directory, load_rules(rules) if rules else DEFAULT_RULES, auto_organize, console=console)
        console.print(f"Watching {directory} (Ctrl+C to stop)")
        run_watch(directory, handler, recursive)


# --------------------------------------------------------------------------- integrity
@integrity_app.command("baseline")
def integrity_baseline(directory: Path, out: Path = typer.Option(Path("baseline.json"), "--out", "-o")) -> None:
    """Record SHA-256 hashes of every file under DIRECTORY."""
    _require_dir(directory)
    count = integrity_mod.create_baseline(directory, out)
    console.print(f"Recorded {count} file(s) in {out}")


@integrity_app.command("verify")
def integrity_verify(directory: Path, baseline: Path = typer.Option(Path("baseline.json"), "--baseline", "-b")) -> None:
    """Compare DIRECTORY with a baseline. Exit code 1 if anything changed (cron/CI friendly)."""
    _require_dir(directory)
    with guard():
        report = integrity_mod.verify(directory, baseline)
    for label, items, color in (("modified", report.modified, "red"), ("removed", report.removed, "yellow"), ("added", report.added, "cyan")):
        for item in items:
            console.print(f"[{color}]{label:<9}[/{color}] {item}")
    if report.clean:
        console.print("[green]No changes since baseline.[/green]")
    else:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()

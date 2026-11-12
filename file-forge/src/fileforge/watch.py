from __future__ import annotations

import time
from pathlib import Path
from typing import Callable

from rich.console import Console
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .journal import apply_moves
from .organize import PARTIAL_DOWNLOAD_EXTS, plan_organize


def wait_until_stable(
    path: Path,
    checks: int = 3,
    interval: float = 0.5,
    timeout: float = 60,
    sleep: Callable[[float], None] = time.sleep,
) -> bool:
    """True once the file size stops changing (i.e. the download/copy has finished)."""
    last, stable, waited = -1, 0, 0.0
    while waited <= timeout:
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            return False
        stable = stable + 1 if size == last else 0
        if stable >= checks:
            return True
        last = size
        sleep(interval)
        waited += interval
    return False


class WatchHandler(FileSystemEventHandler):
    """Logs events; optionally organizes new top-level files once they have finished writing."""

    def __init__(
        self,
        root: Path,
        rules=None,
        auto_organize: bool = False,
        journal_dir: Path | None = None,
        console: Console | None = None,
        interval: float = 0.5,
    ):
        self.root = Path(root)
        self.rules = rules
        self.auto_organize = auto_organize
        self.journal_dir = journal_dir
        self.console = console or Console()
        self.interval = interval

    def _log(self, kind: str, path: str) -> None:
        self.console.print(f"[dim]{time.strftime('%H:%M:%S')}[/dim] {kind:<8} {path}")

    def _maybe_organize(self, path: Path) -> None:
        if not self.auto_organize or path.parent != self.root or path.suffix.lower() in PARTIAL_DOWNLOAD_EXTS:
            return
        if not path.exists() or path.name.startswith("."):
            return
        if not wait_until_stable(path, interval=self.interval):
            return
        moves = plan_organize(self.root, self.rules, files=[path])
        done, _ = apply_moves(moves, "watch", self.journal_dir)
        for move in done:
            self._log("organized", f"{move.src.name} -> {move.dst.parent.name}/")

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._log("created", str(event.src_path))
            self._maybe_organize(Path(str(event.src_path)))

    def on_deleted(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._log("deleted", str(event.src_path))

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._log("modified", str(event.src_path))

    def on_moved(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._log("moved", f"{event.src_path} -> {event.dest_path}")
            self._maybe_organize(Path(str(event.dest_path)))  # e.g. foo.crdownload -> foo.pdf


def run_watch(root: Path, handler: WatchHandler, recursive: bool = True) -> None:
    observer = Observer()
    observer.schedule(handler, str(root), recursive=recursive)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()

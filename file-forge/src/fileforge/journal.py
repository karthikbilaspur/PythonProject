"""Every destructive move is journaled so it can be undone."""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .errors import JournalError
from .util import fileforge_home, unique_path


@dataclass
class Move:
    src: Path
    dst: Path


def journals_dir() -> Path:
    return fileforge_home() / "journals"


def write_journal(moves: list[Move], kind: str, journal_dir: Path | None = None) -> Path:
    directory = journal_dir or journals_dir()
    directory.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    path = directory / f"{stamp}-{kind}.json"
    payload = {
        "kind": kind,
        "created": datetime.now().isoformat(timespec="seconds"),
        "undone": False,
        "moves": [{"src": str(m.src), "dst": str(m.dst)} for m in moves],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def apply_moves(
    moves: list[Move], kind: str, journal_dir: Path | None = None
) -> tuple[list[Move], Path | None]:
    """Perform moves, never overwriting. The journal is written even if a move fails midway."""
    done: list[Move] = []
    try:
        for move in moves:
            move.dst.parent.mkdir(parents=True, exist_ok=True)
            dst = unique_path(move.dst)
            shutil.move(str(move.src), str(dst))
            done.append(Move(move.src, dst))
    finally:
        journal = write_journal(done, kind, journal_dir) if done else None
    return done, journal


def list_journals(journal_dir: Path | None = None) -> list[Path]:
    directory = journal_dir or journals_dir()
    return sorted(directory.glob("*.json")) if directory.exists() else []


def _load(path: Path) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise JournalError(f"Cannot read journal {path}: {exc}") from exc


def latest_journal(journal_dir: Path | None = None) -> Path | None:
    for path in reversed(list_journals(journal_dir)):
        if not _load(path).get("undone"):
            return path
    return None


def undo(journal_path: Path) -> tuple[list[Move], list[tuple[Move, str]]]:
    """Reverse a journal. Returns (restored, skipped-with-reason)."""
    journal_path = Path(journal_path)
    data = _load(journal_path)
    if data.get("undone"):
        raise JournalError("This journal has already been undone.")
    restored: list[Move] = []
    skipped: list[tuple[Move, str]] = []
    for entry in reversed(data["moves"]):
        move = Move(Path(entry["src"]), Path(entry["dst"]))
        if not move.dst.exists():
            skipped.append((move, "moved file no longer exists"))
        elif move.src.exists():
            skipped.append((move, "original location is occupied"))
        else:
            move.src.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(move.dst), str(move.src))
            restored.append(move)
            try:
                move.dst.parent.rmdir()  # only succeeds if now empty
            except OSError:
                pass
    data["undone"] = True
    journal_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return restored, skipped

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable

import yaml

from .journal import Move
from .util import iter_files

DEFAULT_RULES: dict[str, list[str]] = {
    "Documents": [".txt", ".md", ".doc", ".docx", ".pdf", ".rtf", ".odt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".heic"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".webm"],
    "Audio": [".mp3", ".wav", ".ogg", ".flac", ".m4a"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp", ".key"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs", ".html", ".css", ".json"],
}
FALLBACK = "Other"
PARTIAL_DOWNLOAD_EXTS = {".part", ".crdownload", ".tmp", ".download"}


def load_rules(path: str | Path) -> dict[str, list[str]]:
    """YAML mapping of category -> list of extensions."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return {
        cat: [("." + e.lstrip(".")).lower() for e in exts] for cat, exts in raw.items()
    }


def category_for(path: Path, rules: dict[str, list[str]]) -> str:
    ext = path.suffix.lower()
    for category, exts in rules.items():
        if ext in exts:
            return category
    return FALLBACK


def plan_organize(
    root: str | Path,
    rules: dict[str, list[str]] | None = None,
    recursive: bool = False,
    by_date: bool = False,
    files: Iterable[Path] | None = None,
) -> list[Move]:
    """Compute moves without touching anything (this is the dry-run)."""
    root = Path(root)
    rules = rules or DEFAULT_RULES
    category_dirs = set(rules) | {FALLBACK}
    candidates = files if files is not None else iter_files(root, recursive, skip_dirs=category_dirs)
    moves: list[Move] = []
    for path in candidates:
        if path.suffix.lower() in PARTIAL_DOWNLOAD_EXTS:
            continue
        target_dir = root / category_for(path, rules)
        if by_date:
            target_dir = target_dir / datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m")
        if path.parent == target_dir:
            continue
        moves.append(Move(path, target_dir / path.name))
    return moves

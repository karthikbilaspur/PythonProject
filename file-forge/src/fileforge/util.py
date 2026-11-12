from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Iterator


def fileforge_home() -> Path:
    """Where journals and indexes live. Override with FILEFORGE_HOME."""
    return Path(os.environ.get("FILEFORGE_HOME") or Path.home() / ".fileforge")


def sha256_file(path: str | Path, chunk: int = 1 << 20, limit: int | None = None) -> str:
    """SHA-256 of a file; if `limit` is set, only the first `limit` bytes are hashed."""
    h = hashlib.sha256()
    remaining = limit
    with open(path, "rb") as fh:
        while True:
            size = chunk if remaining is None else min(chunk, remaining)
            if size == 0:
                break
            data = fh.read(size)
            if not data:
                break
            h.update(data)
            if remaining is not None:
                remaining -= len(data)
    return h.hexdigest()


def unique_path(dest: Path) -> Path:
    """Return dest, or 'name (1).ext', 'name (2).ext'... if dest already exists."""
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    n = 1
    while True:
        candidate = dest.with_name(f"{stem} ({n}){suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def human_size(num: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num) < 1024 or unit == "TB":
            return f"{num:.0f} {unit}" if unit == "B" else f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} TB"


def iter_files(
    root: str | Path,
    recursive: bool = True,
    include_hidden: bool = False,
    skip_dirs: frozenset[str] | set[str] = frozenset(),
) -> Iterator[Path]:
    """Yield regular files (symlinks are skipped) in a stable order."""
    root = Path(root)
    if not recursive:
        for p in sorted(root.iterdir()):
            if p.is_file() and not p.is_symlink() and (include_hidden or not p.name.startswith(".")):
                yield p
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames if d not in skip_dirs and (include_hidden or not d.startswith("."))
        )
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if p.is_symlink() or (not include_hidden and name.startswith(".")):
                continue
            yield p

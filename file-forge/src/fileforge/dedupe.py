from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .journal import Move, apply_moves
from .util import iter_files, sha256_file

PARTIAL_BYTES = 64 * 1024


@dataclass
class DuplicateGroup:
    size: int
    files: list[Path]  # files[0] is the keeper (oldest, then alphabetical)

    @property
    def wasted(self) -> int:
        return self.size * (len(self.files) - 1)


def find_duplicates(root: str | Path, min_size: int = 1, recursive: bool = True) -> list[DuplicateGroup]:
    """Size -> partial hash -> full hash, so most files are never fully read."""
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in iter_files(root, recursive, include_hidden=False, skip_dirs={".fileforge"}):
        size = path.stat().st_size
        if size >= min_size:
            by_size[size].append(path)

    groups: list[DuplicateGroup] = []
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue
        by_partial: dict[str, list[Path]] = defaultdict(list)
        for p in paths:
            by_partial[sha256_file(p, limit=PARTIAL_BYTES)].append(p)
        for candidates in by_partial.values():
            if len(candidates) < 2:
                continue
            by_full: dict[str, list[Path]] = defaultdict(list)
            for p in candidates:
                by_full[sha256_file(p)].append(p)
            for same in by_full.values():
                if len(same) > 1:
                    ordered = sorted(same, key=lambda p: (p.stat().st_mtime, str(p)))
                    groups.append(DuplicateGroup(size, ordered))
    return sorted(groups, key=lambda g: g.wasted, reverse=True)


def quarantine(groups: list[DuplicateGroup], dest_dir: str | Path, journal_dir: Path | None = None):
    """Move every non-keeper into dest_dir (never deletes)."""
    dest_dir = Path(dest_dir)
    moves = [Move(p, dest_dir / p.name) for g in groups for p in g.files[1:]]
    return apply_moves(moves, "dedupe", journal_dir)

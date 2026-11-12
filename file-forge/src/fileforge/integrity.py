"""Hash baseline + verify: detect added, removed and modified files."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .errors import FileForgeError
from .util import iter_files, sha256_file

SKIP = {".fileforge", ".git"}


@dataclass
class IntegrityReport:
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not (self.added or self.removed or self.modified)


def _scan(root: Path) -> dict[str, dict]:
    entries = {}
    for path in iter_files(root, True, include_hidden=True, skip_dirs=SKIP):
        rel = path.relative_to(root).as_posix()
        entries[rel] = {"sha256": sha256_file(path), "size": path.stat().st_size}
    return entries


def create_baseline(root: str | Path, out_file: str | Path) -> int:
    root = Path(root)
    out_file = Path(out_file)
    entries = _scan(root)
    # never record the baseline file itself if it lives inside the tree
    try:
        entries.pop(out_file.resolve().relative_to(root.resolve()).as_posix(), None)
    except ValueError:
        pass
    payload = {"created": datetime.now().isoformat(timespec="seconds"), "root": str(root), "files": entries}
    out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return len(entries)


def verify(root: str | Path, baseline_file: str | Path) -> IntegrityReport:
    root = Path(root)
    try:
        baseline = json.loads(Path(baseline_file).read_text(encoding="utf-8"))["files"]
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        raise FileForgeError(f"Invalid baseline file: {exc}") from exc
    current = _scan(root)
    try:
        current.pop(Path(baseline_file).resolve().relative_to(root.resolve()).as_posix(), None)
    except ValueError:
        pass
    report = IntegrityReport()
    report.added = sorted(set(current) - set(baseline))
    report.removed = sorted(set(baseline) - set(current))
    report.modified = sorted(
        p for p in set(current) & set(baseline) if current[p]["sha256"] != baseline[p]["sha256"]
    )
    return report

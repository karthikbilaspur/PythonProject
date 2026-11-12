"""Signature-based file carving from raw files or disk images.

Boundaries are found by *parsing* each format (JPEG markers, PNG chunks, ZIP end-of-central-directory)
rather than looking for the first footer, so embedded thumbnails don't truncate the real image.
Input is memory-mapped, so multi-GB images are not loaded into RAM.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import mmap
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

from .util import iter_files


@dataclass(frozen=True)
class Signature:
    name: str
    ext: str
    header: bytes
    finder: Callable  # (buf, start, limit) -> end offset or None
    max_size: int
    min_size: int = 64


@dataclass
class CarvedFile:
    source: str
    kind: str
    offset: int
    length: int
    sha256: str
    valid: str  # "valid" | "invalid" | "unchecked"
    path: str


def jpeg_end(buf, start: int, limit: int) -> int | None:
    n = min(len(buf), limit)
    i = start + 2
    while i + 2 <= n:
        if buf[i] != 0xFF:
            return None
        marker = buf[i + 1]
        if marker == 0xFF:
            i += 1
            continue
        if marker == 0x00:
            return None
        if marker == 0xD9:
            return i + 2
        if marker == 0x01 or 0xD0 <= marker <= 0xD8:
            i += 2
            continue
        if i + 4 > n:
            return None
        seglen = (buf[i + 2] << 8) | buf[i + 3]
        if seglen < 2:
            return None
        i += 2 + seglen
        if marker == 0xDA:  # start of scan: skip entropy-coded data to the next real marker
            while True:
                j = buf.find(b"\xff", i, n)
                if j == -1 or j + 1 >= n:
                    return None
                nxt = buf[j + 1]
                if nxt == 0x00 or 0xD0 <= nxt <= 0xD7:
                    i = j + 2
                    continue
                if nxt == 0xFF:
                    i = j + 1
                    continue
                i = j
                break
    return None


def png_end(buf, start: int, limit: int) -> int | None:
    n = min(len(buf), limit)
    i = start + 8
    while i + 12 <= n:
        length = int.from_bytes(buf[i : i + 4], "big")
        ctype = bytes(buf[i + 4 : i + 8])
        if not ctype.isalpha():
            return None
        nxt = i + 12 + length
        if nxt > n:
            return None
        if ctype == b"IEND":
            return nxt
        i = nxt
    return None


def pdf_end(buf, start: int, limit: int) -> int | None:
    n = min(len(buf), limit)
    next_header = buf.find(b"%PDF-", start + 5, n)
    region_end = n if next_header == -1 else next_header
    eof = buf.rfind(b"%%EOF", start, region_end)
    if eof == -1:
        return None
    end = eof + 5
    while end < n and end < eof + 7 and buf[end] in (10, 13):
        end += 1
    return end


def zip_end(buf, start: int, limit: int) -> int | None:
    n = min(len(buf), limit)
    pos = start
    for _ in range(5):  # a few candidates: the first EOCD may belong to a nested zip
        pos = buf.find(b"PK\x05\x06", pos, n)
        if pos == -1 or pos + 22 > n:
            return None
        end = pos + 22 + int.from_bytes(buf[pos + 20 : pos + 22], "little")
        if end <= n:
            try:
                with zipfile.ZipFile(io.BytesIO(bytes(buf[start:end]))) as zf:
                    zf.namelist()
                return end
            except (zipfile.BadZipFile, ValueError):
                pass
        pos += 4
    return None


def _valid_image(data: bytes) -> bool | None:
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        with Image.open(io.BytesIO(data)) as im:
            im.verify()
        return True
    except Exception:
        return False


def _valid_zip(data: bytes) -> bool | None:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            return zf.testzip() is None
    except Exception:
        return False


_MB = 1 << 20
SIGNATURES: dict[str, Signature] = {
    "jpeg": Signature("jpeg", "jpg", b"\xff\xd8\xff", jpeg_end, 50 * _MB),
    "png": Signature("png", "png", b"\x89PNG\r\n\x1a\n", png_end, 50 * _MB),
    "pdf": Signature("pdf", "pdf", b"%PDF-", pdf_end, 100 * _MB),
    "zip": Signature("zip", "zip", b"PK\x03\x04", zip_end, 100 * _MB, min_size=22),
}
_VALIDATORS = {"jpeg": _valid_image, "png": _valid_image, "zip": _valid_zip}


def carve_buffer(
    buf, source: str, out_dir: Path, kinds: list[str] | None, keep_invalid: bool, counter_start: int
) -> tuple[list[CarvedFile], int]:
    results: list[CarvedFile] = []
    rejected = 0
    size = len(buf)
    for kind in kinds or list(SIGNATURES):
        sig = SIGNATURES[kind]
        pos = 0
        while True:
            start = buf.find(sig.header, pos)
            if start == -1:
                break
            end = sig.finder(buf, start, min(size, start + sig.max_size))
            if end is None or end - start < sig.min_size:
                pos = start + 1
                continue
            data = bytes(buf[start:end])
            validator = _VALIDATORS.get(kind)
            verdict = validator(data) if validator else None
            if verdict is False and not keep_invalid:
                rejected += 1
                pos = start + len(sig.header)
                continue
            index = counter_start + len(results) + 1
            target = out_dir / f"carved_{index:05d}_{kind}_0x{start:x}.{sig.ext}"
            target.write_bytes(data)
            results.append(
                CarvedFile(
                    source=source,
                    kind=kind,
                    offset=start,
                    length=len(data),
                    sha256=hashlib.sha256(data).hexdigest(),
                    valid={True: "valid", False: "invalid", None: "unchecked"}[verdict],
                    path=str(target),
                )
            )
            pos = end
    return results, rejected


def carve(
    source: str | Path,
    out_dir: str | Path,
    kinds: list[str] | None = None,
    keep_invalid: bool = False,
) -> tuple[list[CarvedFile], int]:
    """Carve a file, or every file in a directory. Returns (carved files, rejected candidates)."""
    source, out_dir = Path(source), Path(out_dir)
    unknown = set(kinds or []) - set(SIGNATURES)
    if unknown:
        raise ValueError(f"Unknown file kinds: {', '.join(sorted(unknown))}")
    out_dir.mkdir(parents=True, exist_ok=True)
    sources = [source] if source.is_file() else list(iter_files(source, True, include_hidden=True))
    results: list[CarvedFile] = []
    total_rejected = 0
    for path in sources:
        if path.stat().st_size == 0 or out_dir in path.parents:
            continue
        with open(path, "rb") as fh, mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            found, rejected = carve_buffer(mm, str(path), out_dir, kinds, keep_invalid, len(results))
        results.extend(found)
        total_rejected += rejected
    return results, total_rejected


def write_report(results: list[CarvedFile], out_dir: str | Path) -> tuple[Path, Path]:
    out_dir = Path(out_dir)
    json_path, csv_path = out_dir / "report.json", out_dir / "report.csv"
    json_path.write_text(json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8")
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(CarvedFile.__dataclass_fields__))
        writer.writeheader()
        for r in results:
            writer.writerow(asdict(r))
    return json_path, csv_path

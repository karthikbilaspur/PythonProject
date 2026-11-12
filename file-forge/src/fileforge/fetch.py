"""Resumable downloads: Range requests, .part files, retries, optional SHA-256 check."""
from __future__ import annotations

import hashlib
import os
import re
import time
from pathlib import Path
from typing import Callable
from urllib.parse import unquote, urlparse

import httpx

from .errors import FetchError
from .util import sha256_file

Progress = Callable[[int, int | None], None]
_UNSAFE = re.compile(r'[\\/:*?"<>|\x00-\x1f]')


def _clean_name(name: str) -> str:
    name = _UNSAFE.sub("_", os.path.basename(name.strip().replace("\\", "/"))).strip(". ")
    return name or "download"


def filename_from_url(url: str) -> str:
    return _clean_name(unquote(Path(urlparse(url).path).name))


def filename_from_disposition(header: str | None) -> str | None:
    if not header:
        return None
    match = re.search(r"filename\*\s*=\s*[^']*'[^']*'([^;]+)", header, re.I)
    if match:
        return _clean_name(unquote(match.group(1)))
    match = re.search(r'filename\s*=\s*"?([^";]+)"?', header, re.I)
    return _clean_name(match.group(1)) if match else None


def download(
    url: str,
    dest_dir: str | Path = ".",
    *,
    filename: str | None = None,
    sha256: str | None = None,
    client: httpx.Client | None = None,
    retries: int = 3,
    progress: Progress | None = None,
    sleep: Callable[[float], None] = time.sleep,
    timeout: float = 30,
) -> Path:
    if urlparse(url).scheme not in ("http", "https"):
        raise FetchError(f"Only http(s) URLs are supported: {url}")
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    part = dest_dir / ((_clean_name(filename) if filename else filename_from_url(url)) + ".part")

    owns_client = client is None
    client = client or httpx.Client(follow_redirects=True, timeout=timeout)
    final_name = _clean_name(filename) if filename else None
    try:
        attempt = 0
        while True:
            try:
                final_name = _attempt(client, url, part, final_name, filename is not None, progress)
                break
            except httpx.TransportError as exc:
                attempt += 1
                if attempt > retries:
                    raise FetchError(f"Network error after {retries} retries: {exc}") from exc
                sleep(min(2 ** attempt, 30))  # next attempt resumes from the .part file
    finally:
        if owns_client:
            client.close()

    final = dest_dir / final_name
    if final.exists():
        stem, suffix, n = final.stem, final.suffix, 1
        while final.exists():
            final = dest_dir / f"{stem} ({n}){suffix}"
            n += 1
    os.replace(part, final)
    if sha256 and sha256_file(final) != sha256.lower():
        final.unlink()
        raise FetchError("SHA-256 mismatch: the downloaded file was discarded")
    return final


def _attempt(client, url, part: Path, final_name, name_is_fixed, progress) -> str:
    offset = part.stat().st_size if part.exists() else 0
    headers = {"Range": f"bytes={offset}-"} if offset else {}
    with client.stream("GET", url, headers=headers) as response:
        if response.status_code == 416 and offset:
            return final_name or filename_from_url(url)  # .part already holds the whole file
        if response.status_code >= 400:
            raise FetchError(f"HTTP {response.status_code} for {url}")
        resumed = response.status_code == 206
        if offset and not resumed:
            offset = 0  # server ignored Range: start over
        length = response.headers.get("content-length")
        total = (int(length) + offset) if length and length.isdigit() else None
        if not name_is_fixed:
            final_name = filename_from_disposition(response.headers.get("content-disposition")) or filename_from_url(url)
        done = offset
        with open(part, "ab" if resumed else "wb") as fh:
            for chunk in response.iter_bytes(64 * 1024):
                fh.write(chunk)
                done += len(chunk)
                if progress:
                    progress(done, total)
    return final_name

"""Password-based file encryption: scrypt + chunked AES-256-GCM.

File layout:  header (36 bytes) | chunk_0 | chunk_1 | ...
  header = magic "FFV1", version, scrypt log2(N), r, p, salt(16), nonce prefix(8), chunk size(4)
  each chunk = AES-GCM(plaintext chunk) + 16-byte tag, nonce = prefix || chunk counter,
  AAD = header || final-chunk flag, so reordering, truncation and header tampering are detected.
"""
from __future__ import annotations

import os
import struct
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from .errors import VaultError

MAGIC = b"FFV1"
VERSION = 1
SUFFIX = ".ffv"
TAG = 16
_HEADER = struct.Struct(">4sBBBB16s8sI")
MIN_PASSWORD_LENGTH = 12


def password_issues(password: str) -> list[str]:
    """Human-readable problems with a password (empty list = acceptable)."""
    issues = []
    if len(password) < MIN_PASSWORD_LENGTH:
        issues.append(f"shorter than {MIN_PASSWORD_LENGTH} characters")
    if len(set(password)) <= 2:
        issues.append("uses almost no distinct characters")
    try:  # optional, much better estimator if installed
        from zxcvbn import zxcvbn

        result = zxcvbn(password)
        if result["score"] < 3:
            issues.append("estimated as guessable: " + (result["feedback"].get("warning") or "pick a longer passphrase"))
    except ImportError:
        pass
    return issues


def _key(password: str, salt: bytes, n_log2: int, r: int, p: int) -> bytes:
    return Scrypt(salt=salt, length=32, n=1 << n_log2, r=r, p=p).derive(password.encode("utf-8"))


def _nonce(prefix: bytes, counter: int) -> bytes:
    return prefix + counter.to_bytes(4, "big")


def _aad(header: bytes, final: bool) -> bytes:
    return header + (b"\x01" if final else b"\x00")


def encrypt_file(
    src: str | Path,
    password: str,
    dst: str | Path | None = None,
    *,
    n_log2: int = 15,
    chunk_size: int = 1 << 20,
    overwrite: bool = False,
) -> Path:
    src = Path(src)
    dst = Path(dst) if dst else src.with_name(src.name + SUFFIX)
    if dst.exists() and not overwrite:
        raise VaultError(f"{dst} already exists (use overwrite to replace it)")
    salt, prefix = os.urandom(16), os.urandom(8)
    header = _HEADER.pack(MAGIC, VERSION, n_log2, 8, 1, salt, prefix, chunk_size)
    aead = AESGCM(_key(password, salt, n_log2, 8, 1))
    tmp = dst.with_name(dst.name + ".tmp")
    try:
        with open(src, "rb") as fin, open(tmp, "wb") as fout:
            fout.write(header)
            counter = 0
            chunk = fin.read(chunk_size)
            while True:
                nxt = fin.read(chunk_size)
                final = not nxt
                fout.write(aead.encrypt(_nonce(prefix, counter), chunk, _aad(header, final)))
                if final:
                    break
                chunk, counter = nxt, counter + 1
        os.replace(tmp, dst)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return dst


def decrypt_file(
    src: str | Path,
    password: str,
    dst: str | Path | None = None,
    *,
    overwrite: bool = False,
) -> Path:
    src = Path(src)
    if dst is None:
        dst = src.with_name(src.name[: -len(SUFFIX)]) if src.name.endswith(SUFFIX) else src.with_name(src.name + ".dec")
    dst = Path(dst)
    if dst.exists() and not overwrite:
        raise VaultError(f"{dst} already exists (use overwrite to replace it)")

    tmp = dst.with_name(dst.name + ".tmp")
    try:
        with open(src, "rb") as fin:
            header = fin.read(_HEADER.size)
            if len(header) < _HEADER.size:
                raise VaultError("Not a FileForge vault file (too short)")
            magic, version, n_log2, r, p, salt, prefix, chunk_size = _HEADER.unpack(header)
            if magic != MAGIC or version != VERSION:
                raise VaultError("Not a FileForge vault file (bad header)")
            if not (10 <= n_log2 <= 20 and 1 <= r <= 32 and 1 <= p <= 16 and 0 < chunk_size <= 64 << 20):
                raise VaultError("Vault header has unreasonable parameters")
            aead = AESGCM(_key(password, salt, n_log2, r, p))
            enc_size = chunk_size + TAG
            with open(tmp, "wb") as fout:
                counter = 0
                block = fin.read(enc_size)
                if not block:
                    raise VaultError("Vault file is truncated")
                while True:
                    nxt = fin.read(enc_size)
                    final = not nxt
                    try:
                        fout.write(aead.decrypt(_nonce(prefix, counter), block, _aad(header, final)))
                    except InvalidTag as exc:
                        raise VaultError("Wrong password, or the file is corrupted/tampered with") from exc
                    if final:
                        break
                    block, counter = nxt, counter + 1
        os.replace(tmp, dst)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return dst

"""Incremental hybrid (BM25 + dense embeddings) search over file *contents*, stored in SQLite."""
from __future__ import annotations

import math
import re
import sqlite3
import zlib
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import numpy as np

from .util import iter_files

TEXT_EXTS = {".txt", ".md", ".rst", ".py", ".js", ".ts", ".java", ".c", ".cpp", ".go", ".rs",
             ".json", ".yaml", ".yml", ".toml", ".csv", ".html", ".css", ".ini", ".cfg", ".log", ".tex"}
DOC_EXTS = {".pdf", ".docx"}
SKIP_DIRS = {".git", ".fileforge", "node_modules", "__pycache__", ".venv", "venv"}
MAX_TEXT_BYTES = 5 * 1024 * 1024
_TOKEN = re.compile(r"\w+", re.UNICODE)


class Embedder(Protocol):
    name: str

    def embed(self, texts: list[str]) -> np.ndarray: ...


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.name = model_name
        self._model = None

    def embed(self, texts: list[str]) -> np.ndarray:
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError("Dense search needs: pip install 'fileforge[search]'") from exc
            self._model = SentenceTransformer(self.name)
        return np.asarray(
            self._model.encode(texts, normalize_embeddings=True, convert_to_numpy=True), dtype=np.float32
        )


class HashingEmbedder:
    """Deterministic bag-of-words hashing embedder: no downloads, used for tests and offline demos."""

    def __init__(self, dim: int = 256):
        self.dim = dim
        self.name = f"hashing-{dim}"

    def embed(self, texts: list[str]) -> np.ndarray:
        out = np.zeros((len(texts), self.dim), dtype=np.float32)
        for row, text in enumerate(texts):
            for token in _TOKEN.findall(text.lower()):
                out[row, zlib.crc32(token.encode()) % self.dim] += 1.0
        norms = np.linalg.norm(out, axis=1, keepdims=True)
        return out / np.where(norms == 0, 1, norms)


def extract_text(path: Path) -> str | None:
    """Text of a file, or None if unsupported / the optional library is missing."""
    ext = path.suffix.lower()
    try:
        if ext in TEXT_EXTS:
            if path.stat().st_size > MAX_TEXT_BYTES:
                return None
            return path.read_text(encoding="utf-8", errors="replace")
        if ext == ".pdf":
            from pypdf import PdfReader

            return "\n".join((page.extract_text() or "") for page in PdfReader(str(path)).pages)
        if ext == ".docx":
            from docx import Document

            return "\n".join(p.text for p in Document(str(path)).paragraphs)
    except ImportError:
        return None
    except Exception:
        return None
    return None


def chunk_text(text: str, size: int = 200, overlap: int = 40) -> list[str]:
    words = text.split()
    if not words:
        return []
    step = max(1, size - overlap)
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start : start + size]))
        if start + size >= len(words):
            break
    return chunks


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tf = [Counter(d) for d in docs]
        self.lengths = [len(d) for d in docs]
        self.avg = (sum(self.lengths) / len(docs)) if docs else 0.0
        self.df: Counter = Counter()
        for counts in self.tf:
            self.df.update(counts.keys())
        self.n = len(docs)

    def scores(self, query: list[str]) -> list[float]:
        out = [0.0] * self.n
        for term in set(query):
            df = self.df.get(term, 0)
            if not df:
                continue
            idf = math.log(1 + (self.n - df + 0.5) / (df + 0.5))
            for i, counts in enumerate(self.tf):
                f = counts.get(term, 0)
                if f:
                    denom = f + self.k1 * (1 - self.b + self.b * self.lengths[i] / (self.avg or 1))
                    out[i] += idf * f * (self.k1 + 1) / denom
        return out


@dataclass
class Hit:
    path: str
    chunk: int
    score: float
    snippet: str


class Index:
    def __init__(self, db_path: str | Path, embedder: Embedder | None = None):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.embedder = embedder
        self.db = sqlite3.connect(self.db_path)
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
            CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, mtime REAL, size INTEGER);
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY, path TEXT, idx INTEGER, text TEXT, embedding BLOB,
                FOREIGN KEY(path) REFERENCES files(path) ON DELETE CASCADE);
            CREATE INDEX IF NOT EXISTS chunks_path ON chunks(path);
            """
        )
        self.db.execute("PRAGMA foreign_keys = ON")

    def close(self) -> None:
        self.db.close()

    def stored_embedder(self) -> str | None:
        row = self.db.execute("SELECT value FROM meta WHERE key='embedder'").fetchone()
        return row[0] if row and row[0] else None

    def _sync_embedder_meta(self) -> None:
        wanted = self.embedder.name if self.embedder else ""
        if (self.stored_embedder() or "") != wanted:
            # embeddings from a different model are incomparable: rebuild everything
            self.db.execute("DELETE FROM chunks")
            self.db.execute("DELETE FROM files")
            self.db.execute("INSERT OR REPLACE INTO meta VALUES ('embedder', ?)", (wanted,))
            self.db.commit()

    def update(self, root: str | Path) -> dict[str, int]:
        root = Path(root).resolve()
        self._sync_embedder_meta()
        stats = {"added": 0, "updated": 0, "removed": 0, "unchanged": 0, "skipped": 0}
        seen: set[str] = set()
        for path in iter_files(root, True, skip_dirs=SKIP_DIRS):
            if path.suffix.lower() not in TEXT_EXTS | DOC_EXTS:
                continue
            key = str(path)
            st = path.stat()
            row = self.db.execute("SELECT mtime, size FROM files WHERE path=?", (key,)).fetchone()
            if row and row[0] == st.st_mtime and row[1] == st.st_size:
                seen.add(key)
                stats["unchanged"] += 1
                continue
            text = extract_text(path)
            chunks = chunk_text(text) if text else []
            if not chunks:
                stats["skipped"] += 1
                continue
            seen.add(key)
            vectors = self.embedder.embed(chunks) if self.embedder else None
            self.db.execute("DELETE FROM chunks WHERE path=?", (key,))
            self.db.execute("INSERT OR REPLACE INTO files VALUES (?,?,?)", (key, st.st_mtime, st.st_size))
            for i, chunk in enumerate(chunks):
                blob = vectors[i].astype(np.float32).tobytes() if vectors is not None else None
                self.db.execute("INSERT INTO chunks (path, idx, text, embedding) VALUES (?,?,?,?)", (key, i, chunk, blob))
            stats["updated" if row else "added"] += 1

        prefix = str(root) + "/"
        for (path,) in self.db.execute("SELECT path FROM files").fetchall():
            inside = path.startswith(prefix) or path.startswith(str(root) + "\\")
            if inside and path not in seen:
                self.db.execute("DELETE FROM chunks WHERE path=?", (path,))
                self.db.execute("DELETE FROM files WHERE path=?", (path,))
                stats["removed"] += 1
        self.db.commit()
        return stats

    def search(self, query: str, top_k: int = 5, candidates: int = 50) -> list[Hit]:
        rows = self.db.execute("SELECT path, idx, text, embedding FROM chunks ORDER BY id").fetchall()
        if not rows:
            return []
        fused: dict[int, float] = {}

        tokens = [_TOKEN.findall(r[2].lower()) for r in rows]
        bm25 = BM25(tokens).scores(_TOKEN.findall(query.lower()))
        ranked = [i for i in sorted(range(len(rows)), key=lambda i: -bm25[i]) if bm25[i] > 0][:candidates]
        for rank, i in enumerate(ranked):
            fused[i] = fused.get(i, 0.0) + 1.0 / (60 + rank)

        if self.embedder and all(r[3] is not None for r in rows):
            matrix = np.vstack([np.frombuffer(r[3], dtype=np.float32) for r in rows])
            sims = matrix @ self.embedder.embed([query])[0]
            for rank, i in enumerate(np.argsort(-sims)[:candidates]):
                if sims[i] > 0:
                    fused[int(i)] = fused.get(int(i), 0.0) + 1.0 / (60 + rank)

        best: dict[str, Hit] = {}
        for i, score in sorted(fused.items(), key=lambda kv: -kv[1]):
            path, idx, text, _ = rows[i]
            if path not in best:
                snippet = text if len(text) <= 240 else text[:237] + "..."
                best[path] = Hit(path, idx, score, snippet)
            if len(best) >= top_k:
                break
        return list(best.values())

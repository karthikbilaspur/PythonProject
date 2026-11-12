import os

from fileforge.search import BM25, HashingEmbedder, Index, chunk_text
from conftest import write


def _docs(tmp_path):
    write(tmp_path / "cats.txt", "Cats are small carnivorous feline pets. Cats purr and sleep most of the day.")
    write(tmp_path / "tax.md", "Tax deduction rules: you may deduct home office expenses from taxable income.")
    write(tmp_path / "notes" / "bread.txt", "Sourdough bread needs flour water salt and a long fermentation.")
    write(tmp_path / "image.png", b"\x89PNG not text")


def test_chunking_and_bm25_basics():
    text = " ".join(f"w{i}" for i in range(450))
    chunks = chunk_text(text, size=200, overlap=40)
    assert len(chunks) == 3 and chunks[0].split()[-40:] == chunks[1].split()[:40]
    bm = BM25([["cat", "sat"], ["dog", "ran"], ["cat", "cat", "ran"]])
    scores = bm.scores(["cat"])
    assert scores[1] == 0 and scores[2] > 0 and scores[0] > 0


def test_bm25_only_search(tmp_path):
    _docs(tmp_path)
    index = Index(tmp_path / "idx.db")
    stats = index.update(tmp_path)
    assert stats["added"] == 3  # png ignored
    hits = index.search("fermentation flour")
    assert hits[0].path.endswith("bread.txt")
    assert index.search("zzzzqqq") == []


def test_hybrid_search_with_embedder(tmp_path):
    _docs(tmp_path)
    index = Index(tmp_path / "idx.db", HashingEmbedder())
    index.update(tmp_path)
    hits = index.search("home office tax deduction")
    assert hits[0].path.endswith("tax.md")
    assert len({h.path for h in hits}) == len(hits)  # one hit per file


def test_incremental_update(tmp_path):
    _docs(tmp_path)
    index = Index(tmp_path / "idx.db")
    index.update(tmp_path)
    assert index.update(tmp_path) == {"added": 0, "updated": 0, "removed": 0, "unchanged": 3, "skipped": 0}

    f = tmp_path / "cats.txt"
    f.write_text("Dogs are loyal canine companions that love long walks.")
    os.utime(f, (f.stat().st_atime, f.stat().st_mtime + 10))
    (tmp_path / "tax.md").unlink()
    stats = index.update(tmp_path)
    assert stats["updated"] == 1 and stats["removed"] == 1
    assert index.search("canine")[0].path.endswith("cats.txt")
    assert index.search("deduction") == []


def test_switching_embedder_rebuilds(tmp_path):
    _docs(tmp_path)
    Index(tmp_path / "idx.db").update(tmp_path)
    index = Index(tmp_path / "idx.db", HashingEmbedder())
    stats = index.update(tmp_path)
    assert stats["added"] == 3 and index.stored_embedder() == "hashing-256"


def test_update_only_removes_files_under_given_root(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    write(a / "one.txt", "alpha content here")
    write(b / "two.txt", "beta content here")
    index = Index(tmp_path / "idx.db")
    index.update(a)
    index.update(b)
    assert index.update(a)["removed"] == 0
    assert index.search("beta")[0].path.endswith("two.txt")

from fileforge.dedupe import find_duplicates, quarantine
from fileforge.integrity import create_baseline, verify
from conftest import write


def test_finds_exact_duplicates_only(tmp_path):
    write(tmp_path / "a.bin", b"same content")
    write(tmp_path / "sub" / "b.bin", b"same content")
    write(tmp_path / "c.bin", b"same conten!")  # same size, different content
    write(tmp_path / "d.bin", b"unique")
    groups = find_duplicates(tmp_path)
    assert len(groups) == 1
    assert {p.name for p in groups[0].files} == {"a.bin", "b.bin"}
    assert groups[0].wasted == len(b"same content")


def test_same_prefix_different_tail_is_not_duplicate(tmp_path):
    head = b"h" * 70_000  # larger than the partial-hash window
    write(tmp_path / "a", head + b"A")
    write(tmp_path / "b", head + b"B")
    assert find_duplicates(tmp_path) == []


def test_quarantine_keeps_one_copy(tmp_path):
    write(tmp_path / "a.bin", b"dup")
    write(tmp_path / "b.bin", b"dup")
    groups = find_duplicates(tmp_path)
    done, journal = quarantine(groups, tmp_path / "_dupes")
    assert len(done) == 1 and journal
    remaining = [p for p in tmp_path.glob("*.bin")]
    assert len(remaining) == 1


def test_integrity_detects_changes(tmp_path):
    root = tmp_path / "data"
    write(root / "keep.txt", "k")
    write(root / "change.txt", "before")
    write(root / "gone.txt", "g")
    baseline = tmp_path / "baseline.json"
    assert create_baseline(root, baseline) == 3
    assert verify(root, baseline).clean

    (root / "change.txt").write_text("after")
    (root / "gone.txt").unlink()
    write(root / "new.txt", "n")
    report = verify(root, baseline)
    assert report.modified == ["change.txt"]
    assert report.removed == ["gone.txt"]
    assert report.added == ["new.txt"]


def test_baseline_inside_tree_is_not_self_reported(tmp_path):
    write(tmp_path / "a.txt", "a")
    baseline = tmp_path / "baseline.json"
    create_baseline(tmp_path, baseline)
    assert verify(tmp_path, baseline).clean

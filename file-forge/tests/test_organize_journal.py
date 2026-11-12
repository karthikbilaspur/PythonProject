from fileforge.journal import apply_moves, latest_journal, undo
from fileforge.organize import category_for, load_rules, plan_organize, DEFAULT_RULES
from conftest import write


def test_category_for():
    from pathlib import Path
    assert category_for(Path("a.JPG"), DEFAULT_RULES) == "Images"
    assert category_for(Path("a.unknown"), DEFAULT_RULES) == "Other"
    assert category_for(Path("noext"), DEFAULT_RULES) == "Other"


def test_plan_is_dry_run(tmp_path):
    write(tmp_path / "a.txt")
    write(tmp_path / "b.png")
    moves = plan_organize(tmp_path)
    assert {m.dst.parent.name for m in moves} == {"Documents", "Images"}
    assert (tmp_path / "a.txt").exists()  # nothing moved yet


def test_unknown_types_do_not_crash_and_partial_downloads_skipped(tmp_path):
    write(tmp_path / "weird.xyz")
    write(tmp_path / "movie.mp4.crdownload")
    moves = plan_organize(tmp_path)
    assert [m.dst.parent.name for m in moves] == ["Other"]


def test_apply_and_undo_roundtrip(tmp_path):
    write(tmp_path / "a.txt", "hello")
    write(tmp_path / "b.png", "img")
    done, journal = apply_moves(plan_organize(tmp_path), "organize")
    assert (tmp_path / "Documents" / "a.txt").read_text() == "hello"
    assert not (tmp_path / "a.txt").exists()

    restored, skipped = undo(journal)
    assert len(restored) == 2 and not skipped
    assert (tmp_path / "a.txt").read_text() == "hello"
    assert not (tmp_path / "Documents").exists()  # emptied dir removed
    assert latest_journal() is None  # already undone


def test_collisions_never_overwrite(tmp_path):
    write(tmp_path / "Documents" / "a.txt", "old")
    write(tmp_path / "a.txt", "new")
    apply_moves(plan_organize(tmp_path), "organize")
    assert (tmp_path / "Documents" / "a.txt").read_text() == "old"
    assert (tmp_path / "Documents" / "a (1).txt").read_text() == "new"


def test_undo_skips_when_original_location_occupied(tmp_path):
    write(tmp_path / "a.txt", "one")
    _, journal = apply_moves(plan_organize(tmp_path), "organize")
    write(tmp_path / "a.txt", "someone else's file")
    restored, skipped = undo(journal)
    assert not restored and skipped
    assert (tmp_path / "a.txt").read_text() == "someone else's file"


def test_by_date_and_recursive_skips_category_dirs(tmp_path):
    write(tmp_path / "sub" / "x.txt")
    write(tmp_path / "Documents" / "already.txt")
    moves = plan_organize(tmp_path, recursive=True, by_date=True)
    assert [m.src.name for m in moves] == ["x.txt"]
    assert len(moves[0].dst.parent.name) == 7  # YYYY-MM


def test_custom_rules_file(tmp_path):
    rules_file = tmp_path / "rules.yaml"
    rules_file.write_text("Invoices: [pdf, .xlsx]\n")
    assert load_rules(rules_file) == {"Invoices": [".pdf", ".xlsx"]}

import json

from book_manager.cli import main


def test_cli_flow(tmp_path, capsys):
    db = str(tmp_path / "t.db")
    assert main(["--db", db, "add-book", "Clean Code", "Martin", "978-0-13-235088-4"]) == 0
    assert main(["--db", db, "add-member", "Asha", "a@x.com"]) == 0
    capsys.readouterr()
    assert main(["--db", db, "checkout", "1", "1"]) == 0
    assert json.loads(capsys.readouterr().out)["book_title"] == "Clean Code"
    assert main(["--db", db, "checkout", "1", "1"]) == 1     # already on loan
    assert "error:" in capsys.readouterr().err
    assert main(["--db", db, "list-books", "-q", "clean"]) == 0

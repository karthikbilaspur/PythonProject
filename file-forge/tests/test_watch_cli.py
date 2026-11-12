import io

from rich.console import Console
from typer.testing import CliRunner
from watchdog.events import FileCreatedEvent, FileMovedEvent

from fileforge.cli import app
from fileforge.watch import WatchHandler, wait_until_stable
from conftest import write

runner = CliRunner()


def quiet():
    return Console(file=io.StringIO())


def test_wait_until_stable(tmp_path):
    f = write(tmp_path / "a.bin", b"1")
    assert wait_until_stable(f, interval=0, sleep=lambda s: None)
    assert not wait_until_stable(tmp_path / "missing", interval=0, sleep=lambda s: None)

    grow = {"n": 0}

    def sleep_and_grow(_):
        grow["n"] += 1
        f.write_bytes(b"x" * grow["n"])

    assert not wait_until_stable(f, interval=1, timeout=5, sleep=sleep_and_grow)  # never stabilizes


def test_auto_organize_new_file_and_ignores_partials(tmp_path):
    handler = WatchHandler(tmp_path, auto_organize=True, console=quiet(), interval=0)
    a = write(tmp_path / "report.pdf", b"%PDF")
    handler.on_created(FileCreatedEvent(str(a)))
    assert (tmp_path / "Documents" / "report.pdf").exists()

    part = write(tmp_path / "movie.mp4.crdownload", b"...")
    handler.on_created(FileCreatedEvent(str(part)))
    assert part.exists()  # partial download left alone

    final = tmp_path / "movie.mp4"
    part.rename(final)
    handler.on_moved(FileMovedEvent(str(part), str(final)))  # browser renames when finished
    assert (tmp_path / "Videos" / "movie.mp4").exists()


def test_watch_without_auto_organize_only_logs(tmp_path):
    handler = WatchHandler(tmp_path, auto_organize=False, console=quiet(), interval=0)
    f = write(tmp_path / "a.txt")
    handler.on_created(FileCreatedEvent(str(f)))
    assert f.exists()


def test_cli_organize_dry_run_apply_undo(tmp_path):
    write(tmp_path / "a.txt", "hi")
    r = runner.invoke(app, ["organize", str(tmp_path)])
    assert r.exit_code == 0 and "Dry run" in r.output and (tmp_path / "a.txt").exists()

    r = runner.invoke(app, ["organize", str(tmp_path), "--apply"])
    assert r.exit_code == 0 and (tmp_path / "Documents" / "a.txt").exists()

    r = runner.invoke(app, ["undo"])
    assert r.exit_code == 0 and (tmp_path / "a.txt").read_text() == "hi"


def test_cli_vault_roundtrip_and_weak_password(tmp_path):
    f = write(tmp_path / "s.txt", "top secret")
    r = runner.invoke(app, ["vault", "encrypt", str(f)], input="short\nshort\n")
    assert r.exit_code == 1 and "Weak password" in r.output

    good = "a-reasonably-long-passphrase"
    r = runner.invoke(app, ["vault", "encrypt", str(f)], input=f"{good}\n{good}\n")
    assert r.exit_code == 0 and (tmp_path / "s.txt.ffv").exists()

    out = tmp_path / "back.txt"
    r = runner.invoke(app, ["vault", "decrypt", str(tmp_path / "s.txt.ffv"), "-o", str(out)], input="wrong-wrong-wrong\n")
    assert r.exit_code == 1 and not out.exists()
    r = runner.invoke(app, ["vault", "decrypt", str(tmp_path / "s.txt.ffv"), "-o", str(out)], input=f"{good}\n")
    assert r.exit_code == 0 and out.read_text() == "top secret"


def test_cli_integrity_exit_codes(tmp_path):
    root = tmp_path / "d"
    write(root / "a.txt", "a")
    base = tmp_path / "b.json"
    assert runner.invoke(app, ["integrity", "baseline", str(root), "-o", str(base)]).exit_code == 0
    assert runner.invoke(app, ["integrity", "verify", str(root), "-b", str(base)]).exit_code == 0
    (root / "a.txt").write_text("changed")
    r = runner.invoke(app, ["integrity", "verify", str(root), "-b", str(base)])
    assert r.exit_code == 1 and "modified" in r.output


def test_cli_dedupe_and_search(tmp_path):
    write(tmp_path / "a.txt", "duplicate body text")
    write(tmp_path / "b.txt", "duplicate body text")
    r = runner.invoke(app, ["dedupe", str(tmp_path)])
    assert r.exit_code == 0 and "duplicate:" in r.output

    db = tmp_path / "i.db"
    assert runner.invoke(app, ["search", "index", str(tmp_path), "--db", str(db), "--bm25-only"]).exit_code == 0
    r = runner.invoke(app, ["search", "query", "duplicate", "--db", str(db)])
    assert r.exit_code == 0 and ".txt" in r.output


def test_cli_carve(tmp_path):
    import io as _io
    from PIL import Image

    buf = _io.BytesIO()
    Image.effect_noise((40, 40), 50).convert("RGB").save(buf, "PNG")
    write(tmp_path / "disk.img", b"junk" * 100 + buf.getvalue())
    r = runner.invoke(app, ["carve", str(tmp_path / "disk.img"), "-o", str(tmp_path / "out")])
    assert r.exit_code == 0 and (tmp_path / "out" / "report.json").exists()

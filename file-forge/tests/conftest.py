import pytest


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch):
    """Journals and indexes go to a temp dir, never the real home."""
    home = tmp_path / "ff_home"
    monkeypatch.setenv("FILEFORGE_HOME", str(home))
    return home


def write(path, content=b"x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content if isinstance(content, bytes) else content.encode())
    return path

import hashlib

import httpx
import pytest

from fileforge.errors import FetchError
from fileforge.fetch import download, filename_from_disposition, filename_from_url

BODY = bytes(range(256)) * 40  # 10240 bytes


def make_client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def server(headers=None, status_override=None):
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.headers.get("range"))
        extra = dict(headers or {})
        rng = request.headers.get("range")
        if rng:
            start = int(rng.split("=")[1].split("-")[0])
            return httpx.Response(206, content=BODY[start:], headers={**extra, "content-range": f"bytes {start}-{len(BODY)-1}/{len(BODY)}"})
        return httpx.Response(200, content=BODY, headers=extra)

    return handler, calls


def test_filename_helpers():
    assert filename_from_url("https://x.org/a/b/report%20v2.pdf?x=1") == "report v2.pdf"
    assert filename_from_url("https://x.org/") == "download"
    assert filename_from_disposition('attachment; filename="../../evil.sh"') == "evil.sh"
    assert filename_from_disposition("attachment; filename*=UTF-8''na%C3%AFve.txt") == "naïve.txt"
    assert filename_from_disposition(None) is None


def test_basic_download_uses_content_disposition(tmp_path):
    handler, _ = server({"content-disposition": 'attachment; filename="real-name.bin"'})
    out = download("https://x.org/dl?id=1", tmp_path, client=make_client(handler))
    assert out.name == "real-name.bin" and out.read_bytes() == BODY
    assert not list(tmp_path.glob("*.part"))


def test_resumes_from_part_file(tmp_path):
    (tmp_path / "file.bin.part").write_bytes(BODY[:4000])
    handler, calls = server()
    out = download("https://x.org/file.bin", tmp_path, client=make_client(handler))
    assert calls == ["bytes=4000-"]
    assert out.read_bytes() == BODY


def test_server_ignoring_range_restarts(tmp_path):
    (tmp_path / "file.bin.part").write_bytes(b"stale-partial")
    handler = lambda request: httpx.Response(200, content=BODY)
    out = download("https://x.org/file.bin", tmp_path, client=make_client(handler))
    assert out.read_bytes() == BODY


def test_retries_then_resumes_after_network_error(tmp_path):
    state = {"n": 0}
    inner, calls = server()

    def flaky(request):
        state["n"] += 1
        if state["n"] == 1:
            raise httpx.ConnectError("boom")
        return inner(request)

    sleeps = []
    out = download("https://x.org/file.bin", tmp_path, client=make_client(flaky), sleep=sleeps.append)
    assert out.read_bytes() == BODY and len(sleeps) == 1


def test_gives_up_after_retries(tmp_path):
    def always_down(request):
        raise httpx.ConnectError("down")

    with pytest.raises(FetchError, match="retries"):
        download("https://x.org/f", tmp_path, client=make_client(always_down), retries=2, sleep=lambda s: None)


def test_http_error_and_bad_scheme(tmp_path):
    with pytest.raises(FetchError, match="404"):
        download("https://x.org/f", tmp_path, client=make_client(lambda r: httpx.Response(404)))
    with pytest.raises(FetchError, match="http"):
        download("ftp://x.org/f", tmp_path)


def test_checksum(tmp_path):
    handler, _ = server()
    good = hashlib.sha256(BODY).hexdigest()
    assert download("https://x.org/a.bin", tmp_path, sha256=good, client=make_client(handler)).exists()
    with pytest.raises(FetchError, match="mismatch"):
        download("https://x.org/b.bin", tmp_path, sha256="0" * 64, client=make_client(handler))
    assert not (tmp_path / "b.bin").exists()


def test_existing_file_not_overwritten(tmp_path):
    (tmp_path / "a.bin").write_bytes(b"mine")
    handler, _ = server()
    out = download("https://x.org/a.bin", tmp_path, client=make_client(handler))
    assert out.name == "a (1).bin" and (tmp_path / "a.bin").read_bytes() == b"mine"

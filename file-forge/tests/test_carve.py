import io
import struct
import zipfile

import pytest
from PIL import Image

from fileforge.carve import carve, jpeg_end, png_end, write_report
from conftest import write


def _jpeg(color=(200, 30, 30), size=(64, 64)) -> bytes:
    buf = io.BytesIO()
    Image.effect_noise(size, 60).convert("RGB").save(buf, "JPEG")
    return buf.getvalue()


def _png() -> bytes:
    buf = io.BytesIO()
    Image.effect_noise((48, 48), 50).convert("RGB").save(buf, "PNG")
    return buf.getvalue()


def _jpeg_with_embedded_thumbnail(thumb: bytes) -> bytes:
    outer = _jpeg(size=(128, 128))
    app1 = b"\xff\xe1" + struct.pack(">H", len(thumb) + 2) + thumb
    return outer[:2] + app1 + outer[2:]


def _pdf() -> bytes:
    return b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF\n"


def _zip() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("hello.txt", "hello world " * 20)
    return buf.getvalue()


def test_jpeg_end_ignores_embedded_thumbnail():
    thumb = _jpeg(size=(16, 16))
    outer = _jpeg_with_embedded_thumbnail(thumb)
    assert jpeg_end(outer, 0, len(outer)) == len(outer)
    # a naive "first FFD9" search would stop inside the thumbnail:
    assert outer.find(b"\xff\xd9") + 2 < len(outer)


def test_png_end():
    png = _png()
    assert png_end(png, 0, len(png)) == len(png)


def test_carves_all_formats_from_a_blob(tmp_path):
    thumb = _jpeg(size=(16, 16))
    jpg = _jpeg_with_embedded_thumbnail(thumb)
    png, pdf, zp = _png(), _pdf(), _zip()
    junk = b"\x00\x13\x37" * 500
    image = junk + jpg + junk + png + junk + pdf + junk + zp + junk
    write(tmp_path / "disk.img", image)

    results, rejected = carve(tmp_path / "disk.img", tmp_path / "out")
    by_kind = {r.kind: r for r in results}
    assert set(by_kind) == {"jpeg", "png", "pdf", "zip"}
    assert by_kind["jpeg"].length == len(jpg)  # whole image, thumbnail not carved separately
    assert by_kind["jpeg"].offset == len(junk)
    assert open(by_kind["png"].path, "rb").read() == png
    assert open(by_kind["pdf"].path, "rb").read() == pdf
    assert open(by_kind["zip"].path, "rb").read() == zp
    assert all(r.valid != "invalid" for r in results)


def test_invalid_candidates_are_rejected(tmp_path):
    fake = b"\xff\xd8\xff\xe0" + b"garbage" * 50 + b"\xff\xd9"
    write(tmp_path / "x.bin", b"\x00" * 100 + fake + b"\x00" * 100)
    results, rejected = carve(tmp_path / "x.bin", tmp_path / "out")
    assert results == []


def test_kind_filter_and_unknown_kind(tmp_path):
    write(tmp_path / "x.bin", _png() + _pdf())
    results, _ = carve(tmp_path / "x.bin", tmp_path / "out", kinds=["pdf"])
    assert [r.kind for r in results] == ["pdf"]
    with pytest.raises(ValueError):
        carve(tmp_path / "x.bin", tmp_path / "out2", kinds=["exe"])


def test_directory_scan_empty_file_and_report(tmp_path):
    src = tmp_path / "src"
    write(src / "empty.bin", b"")
    write(src / "a.bin", b"pad" + _png())
    results, _ = carve(src, tmp_path / "out")
    assert len(results) == 1
    json_path, csv_path = write_report(results, tmp_path / "out")
    assert json_path.exists() and "sha256" in csv_path.read_text()

import pytest

from fileforge.errors import VaultError
from fileforge.vault import decrypt_file, encrypt_file, password_issues
from conftest import write

FAST = dict(n_log2=10)  # cheap scrypt for tests


def test_roundtrip_multi_chunk(tmp_path):
    data = bytes(range(256)) * 50  # 12.8 KB
    src = write(tmp_path / "secret.bin", data)
    enc = encrypt_file(src, "correct horse battery", chunk_size=1000, **FAST)
    assert enc.name == "secret.bin.ffv"
    assert data[:64] not in enc.read_bytes()
    out = decrypt_file(enc, "correct horse battery", tmp_path / "out.bin")
    assert out.read_bytes() == data
    assert src.read_bytes() == data  # original untouched


def test_empty_and_exact_chunk_multiple(tmp_path):
    for size in (0, 1000, 2000):
        src = write(tmp_path / f"f{size}", b"z" * size)
        enc = encrypt_file(src, "pw-pw-pw-pw-pw", chunk_size=1000, **FAST)
        assert decrypt_file(enc, "pw-pw-pw-pw-pw", tmp_path / f"o{size}").read_bytes() == b"z" * size


def test_wrong_password_fails_cleanly(tmp_path):
    enc = encrypt_file(write(tmp_path / "a", b"data"), "right-password-1", **FAST)
    with pytest.raises(VaultError, match="Wrong password"):
        decrypt_file(enc, "wrong-password-1", tmp_path / "out")
    assert not (tmp_path / "out").exists() and not (tmp_path / "out.tmp").exists()


def test_tampering_and_truncation_detected(tmp_path):
    enc = encrypt_file(write(tmp_path / "a", b"q" * 3000), "right-password-1", chunk_size=1000, **FAST)
    raw = bytearray(enc.read_bytes())

    flipped = tmp_path / "flipped.ffv"
    raw2 = bytearray(raw)
    raw2[-1] ^= 1
    flipped.write_bytes(raw2)
    with pytest.raises(VaultError):
        decrypt_file(flipped, "right-password-1", tmp_path / "o1")

    truncated = tmp_path / "trunc.ffv"
    truncated.write_bytes(raw[: 36 + 2 * (1000 + 16)])  # drop the final chunk
    with pytest.raises(VaultError):
        decrypt_file(truncated, "right-password-1", tmp_path / "o2")


def test_same_input_encrypts_differently(tmp_path):
    src = write(tmp_path / "a", b"same")
    a = encrypt_file(src, "right-password-1", tmp_path / "1.ffv", **FAST).read_bytes()
    b = encrypt_file(src, "right-password-1", tmp_path / "2.ffv", **FAST).read_bytes()
    assert a != b  # fresh salt and nonce prefix every time


def test_refuses_to_overwrite_and_rejects_non_vault(tmp_path):
    src = write(tmp_path / "a", b"x")
    encrypt_file(src, "right-password-1", **FAST)
    with pytest.raises(VaultError, match="already exists"):
        encrypt_file(src, "right-password-1", **FAST)
    with pytest.raises(VaultError, match="Not a FileForge"):
        decrypt_file(write(tmp_path / "plain.ffv", b"not a vault file at all, just text....."), "x" * 12)


def test_password_issues():
    assert password_issues("short")
    assert password_issues("aaaaaaaaaaaaaaaa")
    assert password_issues("a-reasonably-long-passphrase") == []

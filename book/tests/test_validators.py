import pytest

from book_manager.exceptions import ValidationError
from book_manager.validators import clean_email, clean_int, normalize_isbn


def test_isbn13_and_10_valid():
    assert normalize_isbn("978-0-13-235088-4") == "9780132350884"
    assert normalize_isbn("0-306-40615-2") == "0306406152"
    assert normalize_isbn("080442957x") == "080442957X"


@pytest.mark.parametrize("bad", ["9780132350885", "123", "abcdefghij", None, ""])
def test_isbn_invalid(bad):
    with pytest.raises(ValidationError):
        normalize_isbn(bad)


def test_email_and_int():
    assert clean_email(" A@B.com ") == "a@b.com"
    with pytest.raises(ValidationError):
        clean_email("nope")
    with pytest.raises(ValidationError):
        clean_int(True, "copies")
    with pytest.raises(ValidationError):
        clean_int(0, "copies")

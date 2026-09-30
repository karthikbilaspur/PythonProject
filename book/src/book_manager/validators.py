"""Input validation helpers (pure functions, easy to test)."""
import re

from .exceptions import ValidationError

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def clean_text(value, field: str, max_len: int = 200) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"'{field}' is required")
    value = value.strip()
    if len(value) > max_len:
        raise ValidationError(f"'{field}' must be at most {max_len} characters")
    return value


def clean_int(value, field: str, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValidationError(f"'{field}' must be an integer >= {minimum}")
    return value


def clean_email(value) -> str:
    value = clean_text(value, "email").lower()
    if not _EMAIL.match(value):
        raise ValidationError("'email' is not a valid address")
    return value


def normalize_isbn(value) -> str:
    """Return a validated ISBN-10 or ISBN-13 without hyphens/spaces."""
    if not isinstance(value, str):
        raise ValidationError("'isbn' is required")
    isbn = value.replace("-", "").replace(" ", "").upper()
    if len(isbn) == 13 and isbn.isdigit():
        total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(isbn))
        ok = total % 10 == 0
    elif len(isbn) == 10 and re.fullmatch(r"\d{9}[\dX]", isbn):
        total = sum((10 - i) * (10 if d == "X" else int(d)) for i, d in enumerate(isbn))
        ok = total % 11 == 0
    else:
        ok = False
    if not ok:
        raise ValidationError(f"'{value}' is not a valid ISBN-10/13")
    return isbn

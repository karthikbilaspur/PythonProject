import pytest

from book_manager.exceptions import ConflictError, NotFoundError, ValidationError


def test_add_and_get(seeded):
    svc, book, _ = seeded
    assert book["isbn"] == "9780132350884" and book["available"] == 2
    assert svc.get_book(book["id"])["title"] == "Clean Code"


def test_duplicate_isbn(seeded):
    svc, _, _ = seeded
    with pytest.raises(ConflictError):
        svc.add_book("Other", "Someone", "9780132350884")


def test_search_pagination_and_wildcards(svc):
    svc.add_book("Python Basics", "A. Author", "9780306406157")
    svc.add_book("Advanced Python", "B. Writer", "0306406152")
    svc.add_book("Cooking 101", "Chef", "080442957X")
    assert svc.list_books(q="python")["total"] == 2
    assert svc.list_books(q="%")["total"] == 0          # '%' is treated literally
    page = svc.list_books(limit=1, offset=1)
    assert page["total"] == 3 and len(page["items"]) == 1


def test_update_rules(seeded):
    svc, book, member = seeded
    other = svc.add_member("Ben", "ben@example.com")
    svc.checkout(member["id"], book["id"])
    svc.checkout(other["id"], book["id"])                      # both copies on loan
    with pytest.raises(ConflictError):
        svc.update_book(book["id"], copies=1)                  # below copies on loan
    assert svc.update_book(book["id"], copies=3)["available"] == 1
    assert svc.update_book(book["id"], title="Clean Code 2e")["title"] == "Clean Code 2e"
    with pytest.raises(ValidationError):
        svc.update_book(book["id"])
    with pytest.raises(NotFoundError):
        svc.update_book(999, title="x")


def test_delete_blocked_by_active_loan(seeded):
    svc, book, member = seeded
    loan = svc.checkout(member["id"], book["id"])
    with pytest.raises(ConflictError):
        svc.delete_book(book["id"])
    svc.return_book(loan["id"])
    svc.delete_book(book["id"])
    with pytest.raises(NotFoundError):
        svc.get_book(book["id"])

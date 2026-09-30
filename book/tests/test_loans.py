from datetime import date

import pytest

from book_manager.exceptions import ConflictError, NotFoundError

D = date(2026, 1, 1)


def test_checkout_and_availability(seeded):
    svc, book, member = seeded
    loan = svc.checkout(member["id"], book["id"], today=D)
    assert loan["due_on"] == "2026-01-15" and svc.get_book(book["id"])["available"] == 1


def test_no_duplicate_loan_and_no_copies(seeded):
    svc, book, member = seeded
    svc.checkout(member["id"], book["id"], today=D)
    with pytest.raises(ConflictError):
        svc.checkout(member["id"], book["id"], today=D)          # same book twice
    other = svc.add_member("Ben", "ben@example.com")
    svc.checkout(other["id"], book["id"], today=D)               # second copy
    third = svc.add_member("Cy", "cy@example.com")
    with pytest.raises(ConflictError):
        svc.checkout(third["id"], book["id"], today=D)           # none left


def test_member_loan_limit(svc):
    member = svc.add_member("Asha", "asha@example.com")
    isbns = ["9780132350884", "0306406152", "080442957X", "9780306406157"]
    books = [svc.add_book(f"B{i}", "A", isbn) for i, isbn in enumerate(isbns)]
    for b in books[:3]:
        svc.checkout(member["id"], b["id"], today=D)
    with pytest.raises(ConflictError):
        svc.checkout(member["id"], books[3]["id"], today=D)


def test_return_fine_and_double_return(seeded):
    svc, book, member = seeded
    loan = svc.checkout(member["id"], book["id"], days=7, today=D)
    done = svc.return_book(loan["id"], today=date(2026, 1, 13))  # due Jan 8 -> 5 days late
    assert done["fine"] == 2.5 and svc.get_book(book["id"])["available"] == 2
    with pytest.raises(ConflictError):
        svc.return_book(loan["id"])


def test_on_time_return_has_no_fine(seeded):
    svc, book, member = seeded
    loan = svc.checkout(member["id"], book["id"], today=D)
    assert svc.return_book(loan["id"], today=date(2026, 1, 15))["fine"] == 0


def test_overdue_report(seeded):
    svc, book, member = seeded
    svc.checkout(member["id"], book["id"], today=D)
    assert svc.overdue_loans(today=date(2026, 1, 15)) == []
    rows = svc.overdue_loans(today=date(2026, 1, 20))
    assert rows[0]["days_overdue"] == 5 and rows[0]["projected_fine"] == 2.5


def test_unknown_ids(seeded):
    svc, book, member = seeded
    with pytest.raises(NotFoundError):
        svc.checkout(999, book["id"])
    with pytest.raises(NotFoundError):
        svc.checkout(member["id"], 999)
    with pytest.raises(NotFoundError):
        svc.return_book(999)

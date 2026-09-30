"""LibraryService: all business rules live here (books, members, loans, fines)."""
import os
import sqlite3
import threading
from contextlib import contextmanager
from datetime import date, timedelta

from . import db
from .exceptions import ConflictError, NotFoundError, ValidationError
from .validators import clean_email, clean_int, clean_text, normalize_isbn

_BOOK_SELECT = """
SELECT b.*, b.total_copies - (
    SELECT COUNT(*) FROM loans l WHERE l.book_id = b.id AND l.returned_on IS NULL
) AS available FROM books b
"""


def _like(term: str) -> str:
    escaped = term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


class LibraryService:
    def __init__(self, db_path: str = ":memory:", fine_per_day: float | None = None,
                 max_loans: int = 3, default_days: int = 14):
        self.conn = db.connect(db_path)
        self.fine_per_day = float(os.getenv("FINE_PER_DAY", "0.5")) if fine_per_day is None else fine_per_day
        self.max_loans = max_loans
        self.default_days = default_days
        self._lock = threading.RLock()

    @contextmanager
    def _tx(self):
        """Write transaction. BEGIN IMMEDIATE takes the write lock up front, so two
        concurrent checkouts can't both take the last copy."""
        with self._lock:
            self.conn.execute("BEGIN IMMEDIATE")
            try:
                yield self.conn
            except BaseException:
                self.conn.execute("ROLLBACK")
                raise
            self.conn.execute("COMMIT")

    def _one(self, sql: str, params=()):
        with self._lock:
            return self.conn.execute(sql, params).fetchone()

    def _all(self, sql: str, params=()):
        with self._lock:
            return self.conn.execute(sql, params).fetchall()

    # ------------------------------------------------------------------ books
    def add_book(self, title, author, isbn, copies=1) -> dict:
        title, author = clean_text(title, "title"), clean_text(author, "author")
        isbn, copies = normalize_isbn(isbn), clean_int(copies, "copies")
        try:
            with self._tx() as c:
                cur = c.execute("INSERT INTO books (title, author, isbn, total_copies) VALUES (?,?,?,?)",
                                (title, author, isbn, copies))
                book_id = cur.lastrowid
        except sqlite3.IntegrityError:
            raise ConflictError(f"A book with ISBN {isbn} already exists") from None
        return self.get_book(book_id)

    def get_book(self, book_id: int) -> dict:
        row = self._one(_BOOK_SELECT + " WHERE b.id = ?", (book_id,))
        if row is None:
            raise NotFoundError(f"Book {book_id} not found")
        return dict(row)

    def list_books(self, q: str | None = None, limit: int = 20, offset: int = 0,
                   available_only: bool = False) -> dict:
        where, params = [], []
        if q:
            where.append("(b.title LIKE ? ESCAPE '\\' OR b.author LIKE ? ESCAPE '\\' OR b.isbn LIKE ? ESCAPE '\\')")
            params += [_like(q)] * 3
        clause = (" WHERE " + " AND ".join(where)) if where else ""
        having = " WHERE available > 0" if available_only else ""
        base = f"SELECT * FROM ({_BOOK_SELECT}{clause}){having}"
        total = self._one(f"SELECT COUNT(*) FROM ({base})", params)[0]
        rows = self._all(base + " ORDER BY title COLLATE NOCASE LIMIT ? OFFSET ?", params + [limit, offset])
        return {"items": [dict(r) for r in rows], "total": total, "limit": limit, "offset": offset}

    def update_book(self, book_id: int, title=None, author=None, copies=None) -> dict:
        if title is None and author is None and copies is None:
            raise ValidationError("Provide at least one of: title, author, copies")
        with self._tx() as c:
            book = c.execute(_BOOK_SELECT + " WHERE b.id = ?", (book_id,)).fetchone()
            if book is None:
                raise NotFoundError(f"Book {book_id} not found")
            new_title = clean_text(title, "title") if title is not None else book["title"]
            new_author = clean_text(author, "author") if author is not None else book["author"]
            new_copies = clean_int(copies, "copies") if copies is not None else book["total_copies"]
            on_loan = book["total_copies"] - book["available"]
            if new_copies < on_loan:
                raise ConflictError(f"{on_loan} copies are on loan; copies cannot be below that")
            c.execute("UPDATE books SET title=?, author=?, total_copies=? WHERE id=?",
                      (new_title, new_author, new_copies, book_id))
        return self.get_book(book_id)

    def delete_book(self, book_id: int) -> None:
        with self._tx() as c:
            if c.execute("SELECT 1 FROM books WHERE id=?", (book_id,)).fetchone() is None:
                raise NotFoundError(f"Book {book_id} not found")
            if c.execute("SELECT 1 FROM loans WHERE book_id=? AND returned_on IS NULL", (book_id,)).fetchone():
                raise ConflictError("Book has active loans and cannot be deleted")
            c.execute("DELETE FROM loans WHERE book_id=?", (book_id,))   # returned-loan history
            c.execute("DELETE FROM books WHERE id=?", (book_id,))

    # ---------------------------------------------------------------- members
    def add_member(self, name, email) -> dict:
        name, email = clean_text(name, "name"), clean_email(email)
        try:
            with self._tx() as c:
                member_id = c.execute("INSERT INTO members (name, email) VALUES (?,?)", (name, email)).lastrowid
        except sqlite3.IntegrityError:
            raise ConflictError(f"A member with email {email} already exists") from None
        return self.get_member(member_id)

    def get_member(self, member_id: int) -> dict:
        row = self._one("SELECT * FROM members WHERE id=?", (member_id,))
        if row is None:
            raise NotFoundError(f"Member {member_id} not found")
        return dict(row)

    def list_members(self) -> list[dict]:
        return [dict(r) for r in self._all("SELECT * FROM members ORDER BY name COLLATE NOCASE")]

    # ------------------------------------------------------------------ loans
    def checkout(self, member_id: int, book_id: int, days: int | None = None, today: date | None = None) -> dict:
        today = today or date.today()
        days = clean_int(days if days is not None else self.default_days, "days")
        with self._tx() as c:
            if c.execute("SELECT 1 FROM members WHERE id=?", (member_id,)).fetchone() is None:
                raise NotFoundError(f"Member {member_id} not found")
            book = c.execute(_BOOK_SELECT + " WHERE b.id = ?", (book_id,)).fetchone()
            if book is None:
                raise NotFoundError(f"Book {book_id} not found")
            active = c.execute("SELECT book_id FROM loans WHERE member_id=? AND returned_on IS NULL",
                               (member_id,)).fetchall()
            if len(active) >= self.max_loans:
                raise ConflictError(f"Member already has {self.max_loans} active loans (the maximum)")
            if any(r["book_id"] == book_id for r in active):
                raise ConflictError("Member already has this book on loan")
            if book["available"] < 1:
                raise ConflictError("No copies available")
            loan_id = c.execute(
                "INSERT INTO loans (book_id, member_id, borrowed_on, due_on) VALUES (?,?,?,?)",
                (book_id, member_id, today.isoformat(), (today + timedelta(days=days)).isoformat())).lastrowid
        return self.get_loan(loan_id)

    def return_book(self, loan_id: int, today: date | None = None) -> dict:
        today = today or date.today()
        with self._tx() as c:
            loan = c.execute("SELECT * FROM loans WHERE id=?", (loan_id,)).fetchone()
            if loan is None:
                raise NotFoundError(f"Loan {loan_id} not found")
            if loan["returned_on"] is not None:
                raise ConflictError("Loan was already returned")
            fine = self._fine(date.fromisoformat(loan["due_on"]), today)
            c.execute("UPDATE loans SET returned_on=?, fine=? WHERE id=?", (today.isoformat(), fine, loan_id))
        return self.get_loan(loan_id)

    def get_loan(self, loan_id: int) -> dict:
        row = self._one(
            "SELECT l.*, b.title AS book_title, m.name AS member_name FROM loans l "
            "JOIN books b ON b.id=l.book_id JOIN members m ON m.id=l.member_id WHERE l.id=?", (loan_id,))
        if row is None:
            raise NotFoundError(f"Loan {loan_id} not found")
        return dict(row)

    def member_loans(self, member_id: int, active_only: bool = False) -> list[dict]:
        self.get_member(member_id)   # 404 if unknown
        sql = ("SELECT l.*, b.title AS book_title FROM loans l JOIN books b ON b.id=l.book_id "
               "WHERE l.member_id=?" + (" AND l.returned_on IS NULL" if active_only else "") +
               " ORDER BY l.borrowed_on DESC, l.id DESC")
        return [dict(r) for r in self._all(sql, (member_id,))]

    def overdue_loans(self, today: date | None = None) -> list[dict]:
        today = today or date.today()
        rows = self._all(
            "SELECT l.*, b.title AS book_title, m.name AS member_name, m.email AS member_email "
            "FROM loans l JOIN books b ON b.id=l.book_id JOIN members m ON m.id=l.member_id "
            "WHERE l.returned_on IS NULL AND l.due_on < ? ORDER BY l.due_on", (today.isoformat(),))
        out = []
        for r in rows:
            d = dict(r)
            d["days_overdue"] = (today - date.fromisoformat(d["due_on"])).days
            d["projected_fine"] = self._fine(date.fromisoformat(d["due_on"]), today)
            out.append(d)
        return out

    def _fine(self, due: date, returned: date) -> float:
        return round(max(0, (returned - due).days) * self.fine_per_day, 2)

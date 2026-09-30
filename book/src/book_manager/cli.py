"""Command-line interface: `book-manager <command>` or `python -m book_manager <command>`."""
import argparse
import json
import os
import sys

from .exceptions import LibraryError
from .service import LibraryService


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="book-manager", description="Manage books, members and loans.")
    p.add_argument("--db", default=os.getenv("BOOKS_DB", "books.db"), help="SQLite file (default: books.db)")
    sub = p.add_subparsers(dest="command", required=True)

    a = sub.add_parser("add-book", help="Add a book")
    a.add_argument("title"); a.add_argument("author"); a.add_argument("isbn")
    a.add_argument("--copies", type=int, default=1)

    s = sub.add_parser("list-books", help="List/search books")
    s.add_argument("-q", "--query"); s.add_argument("--available", action="store_true")
    s.add_argument("--limit", type=int, default=20); s.add_argument("--offset", type=int, default=0)

    m = sub.add_parser("add-member", help="Add a member")
    m.add_argument("name"); m.add_argument("email")

    sub.add_parser("list-members", help="List members")

    c = sub.add_parser("checkout", help="Lend a book")
    c.add_argument("member_id", type=int); c.add_argument("book_id", type=int)
    c.add_argument("--days", type=int)

    r = sub.add_parser("return", help="Return a loan")
    r.add_argument("loan_id", type=int)

    ml = sub.add_parser("member-loans", help="Loans for a member")
    ml.add_argument("member_id", type=int); ml.add_argument("--active", action="store_true")

    sub.add_parser("overdue", help="List overdue loans")
    return p


def run(args, svc: LibraryService):
    cmd = args.command
    if cmd == "add-book":
        return svc.add_book(args.title, args.author, args.isbn, args.copies)
    if cmd == "list-books":
        return svc.list_books(args.query, args.limit, args.offset, args.available)
    if cmd == "add-member":
        return svc.add_member(args.name, args.email)
    if cmd == "list-members":
        return svc.list_members()
    if cmd == "checkout":
        return svc.checkout(args.member_id, args.book_id, args.days)
    if cmd == "return":
        return svc.return_book(args.loan_id)
    if cmd == "member-loans":
        return svc.member_loans(args.member_id, args.active)
    if cmd == "overdue":
        return svc.overdue_loans()
    raise AssertionError(cmd)


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        print(json.dumps(run(args, LibraryService(args.db)), indent=2))
        return 0
    except LibraryError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

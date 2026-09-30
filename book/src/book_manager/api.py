"""Flask API. Thin layer: parse/validate HTTP input, call LibraryService, map errors."""
import hmac
import os

from flask import Flask, jsonify, request

from .exceptions import LibraryError, ValidationError
from .service import LibraryService


def _body() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValidationError("A JSON object body is required")
    return data


def _int_arg(name: str, default: int, minimum: int, maximum: int) -> int:
    raw = request.args.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        raise ValidationError(f"'{name}' must be an integer") from None
    if not minimum <= value <= maximum:
        raise ValidationError(f"'{name}' must be between {minimum} and {maximum}")
    return value


def create_app(service: LibraryService | None = None, api_key: str | None = None) -> Flask:
    app = Flask(__name__)
    svc = service or LibraryService(os.getenv("BOOKS_DB", "books.db"))
    key = api_key or os.getenv("API_KEY")   # optional: if set, every call (except /health) needs it

    @app.before_request
    def authenticate():
        if key and request.endpoint != "health":
            if not hmac.compare_digest(request.headers.get("X-API-Key", ""), key):
                return jsonify(error="unauthorized"), 401

    @app.errorhandler(LibraryError)
    def library_error(e: LibraryError):
        return jsonify(error=str(e)), e.status

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    # ---- books
    @app.post("/books")
    def add_book():
        d = _body()
        return jsonify(svc.add_book(d.get("title"), d.get("author"), d.get("isbn"), d.get("copies", 1))), 201

    @app.get("/books")
    def list_books():
        return jsonify(svc.list_books(
            q=request.args.get("q"), limit=_int_arg("limit", 20, 1, 100),
            offset=_int_arg("offset", 0, 0, 10**9),
            available_only=request.args.get("available") == "true"))

    @app.get("/books/<int:book_id>")
    def get_book(book_id):
        return jsonify(svc.get_book(book_id))

    @app.put("/books/<int:book_id>")
    def update_book(book_id):
        d = _body()
        return jsonify(svc.update_book(book_id, d.get("title"), d.get("author"), d.get("copies")))

    @app.delete("/books/<int:book_id>")
    def delete_book(book_id):
        svc.delete_book(book_id)
        return "", 204

    # ---- members
    @app.post("/members")
    def add_member():
        d = _body()
        return jsonify(svc.add_member(d.get("name"), d.get("email"))), 201

    @app.get("/members")
    def list_members():
        return jsonify(svc.list_members())

    @app.get("/members/<int:member_id>")
    def get_member(member_id):
        return jsonify(svc.get_member(member_id))

    @app.get("/members/<int:member_id>/loans")
    def member_loans(member_id):
        return jsonify(svc.member_loans(member_id, active_only=request.args.get("active") == "true"))

    # ---- loans
    @app.post("/loans")
    def checkout():
        d = _body()
        return jsonify(svc.checkout(d.get("member_id"), d.get("book_id"), d.get("days"))), 201

    @app.post("/loans/<int:loan_id>/return")
    def return_book(loan_id):
        return jsonify(svc.return_book(loan_id))

    @app.get("/loans/overdue")
    def overdue():
        return jsonify(svc.overdue_loans())

    return app


if __name__ == "__main__":  # development server only; use gunicorn in production
    create_app().run(host="127.0.0.1", port=5000)

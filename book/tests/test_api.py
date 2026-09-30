import pytest

from book_manager.api import create_app
from book_manager.service import LibraryService


@pytest.fixture
def client():
    return create_app(LibraryService(":memory:"), api_key="k").test_client()


H = {"X-API-Key": "k"}


def test_auth_and_health(client):
    assert client.get("/health").status_code == 200
    assert client.get("/books").status_code == 401
    assert client.get("/books", headers=H).status_code == 200


def test_full_flow(client):
    r = client.post("/books", json={"title": "Clean Code", "author": "Martin",
                                    "isbn": "978-0-13-235088-4", "copies": 1}, headers=H)
    assert r.status_code == 201
    book_id = r.get_json()["id"]
    member_id = client.post("/members", json={"name": "Asha", "email": "a@x.com"}, headers=H).get_json()["id"]

    loan = client.post("/loans", json={"member_id": member_id, "book_id": book_id}, headers=H)
    assert loan.status_code == 201
    assert client.get("/books?available=true", headers=H).get_json()["total"] == 0
    assert client.post("/loans", json={"member_id": member_id, "book_id": book_id}, headers=H).status_code == 409

    loan_id = loan.get_json()["id"]
    assert client.post(f"/loans/{loan_id}/return", headers=H).status_code == 200
    assert client.get(f"/members/{member_id}/loans?active=true", headers=H).get_json() == []
    assert client.delete(f"/books/{book_id}", headers=H).status_code == 204
    assert client.get(f"/books/{book_id}", headers=H).status_code == 404


def test_validation_errors(client):
    assert client.post("/books", json={"title": "x"}, headers=H).status_code == 400
    assert client.post("/books", data="not json", headers=H).status_code == 400
    assert client.get("/books?limit=abc", headers=H).status_code == 400
    assert client.get("/books?limit=1000", headers=H).status_code == 400

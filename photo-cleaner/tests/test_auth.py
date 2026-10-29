import pytest
from flask.testing import FlaskClient
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Protocol, cast
from app import app, db
from models import User


class _UserAuth(Protocol):
    password_hash: str

    def check_password(self, password: str) -> bool: ...


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

def test_register_and_login(client: FlaskClient):
    # Register
    resp = client.post('/register', data={
        'name': 'Test User',
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'test1234'
    }, follow_redirects=True)
    assert b'Login' in resp.data or resp.status_code == 200

    # Check password is hashed
    with app.app_context():
        session = cast(Session, db.session)
        user = cast(
            _UserAuth | None,
            session.scalar(select(User).where(User.username == 'testuser')),
        )
        assert user is not None
        assert user.password_hash != 'test1234'
        assert user.check_password('test1234') == True
        assert user.check_password('wrong') == False

def test_duplicate_username(client: FlaskClient):
    client.post('/register', data={'name':'A','username':'dup','email':'a@a.com','password':'123456'})
    resp = client.post('/register', data={'name':'B','username':'dup','email':'b@b.com','password':'123456'}, follow_redirects=True)
    assert b'already exists' in resp.data.lower()

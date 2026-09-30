import json

import pytest

from aws_ops.api import create_app
from aws_ops.sqs import SQSService

H = {"X-API-Key": "secret"}


@pytest.fixture
def client(aws):
    return create_app(SQSService("us-east-1"), api_key="secret").test_client()


def test_requires_api_key(client):
    assert client.post("/queues", json={"queue_name": "q"}).status_code == 401


def test_validation(client):
    assert client.post("/queues", json={}, headers=H).status_code == 400


def test_full_flow(client):
    assert client.post("/queues", json={"queue_name": "q"}, headers=H).status_code == 201
    payload = json.dumps({"message": "hello"})
    assert client.post("/queues/q/messages", json={"message_body": payload}, headers=H).status_code == 201
    r = client.post("/queues/q/messages/receive", headers=H)
    assert r.status_code == 200 and r.get_json()["message"] == payload
    assert client.post("/queues/q/messages/receive", headers=H).status_code == 204
    assert client.delete("/queues/q", headers=H).status_code == 204


def test_missing_queue_is_404(client):
    assert client.post("/queues/nope/messages", json={"message_body": "x"}, headers=H).status_code == 404

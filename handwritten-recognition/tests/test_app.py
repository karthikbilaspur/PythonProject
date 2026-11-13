import pytest
from flask.testing import FlaskClient
from unittest.mock import patch
from typing import Any
import app as app_module


@pytest.fixture
def client() -> FlaskClient:
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_index(client: FlaskClient):
    assert client.get("/").status_code == 200


def test_health(client: FlaskClient):
    assert client.get("/health").get_json()["status"] == "ok"


def test_predict_missing(client: FlaskClient):
    assert client.post("/predict", json={}).status_code == 400


def test_predict_bad_mode(client: FlaskClient):
    assert client.post("/predict", json={"image": [255] * 784, "mode": "bad"}).status_code == 400


def test_predict_ok_mocked(client: FlaskClient):
    fake: dict[str, Any] = {"prediction": "7", "confidence": 0.99, "top3": [], "mode": "combined"}
    with patch.object(app_module.predictor, "predict_array", return_value=fake):
        response = client.post("/predict", json={"image": [255] * 784, "mode": "combined"})
        assert response.status_code == 200
        assert response.get_json()["prediction"] == "7"

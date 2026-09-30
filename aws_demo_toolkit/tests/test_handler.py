import json

from aws_ops.handler import lambda_handler


def test_handler_dry_run_ok(aws, monkeypatch):
    monkeypatch.setenv("DRY_RUN", "true")
    monkeypatch.setattr("aws_ops.handler.enabled_regions", lambda: ["us-east-1"])
    resp = lambda_handler({}, None)
    body = json.loads(resp["body"])
    assert resp["statusCode"] == 200 and body["dry_run"] is True and "us-east-1" in body["report"]

"""Flask API over SQSService: validated input, API-key auth, proper status codes."""
import hmac
import os

from botocore.exceptions import ClientError
from flask import Flask, jsonify, request

from .sqs import SQSService


def create_app(sqs_service: SQSService | None = None, api_key: str | None = None) -> Flask:
    app = Flask(__name__)
    service = sqs_service or SQSService(os.getenv("AWS_REGION", "us-east-1"))
    key = api_key or os.getenv("API_KEY")
    if not key:
        raise RuntimeError("API_KEY must be set; refusing to start an unauthenticated API")

    @app.before_request
    def require_key():
        if request.endpoint == "health":
            return None
        supplied = request.headers.get("X-API-Key", "")
        if not hmac.compare_digest(supplied, key):
            return jsonify(error="unauthorized"), 401

    @app.errorhandler(ClientError)
    def aws_error(e: ClientError):
        code = e.response["Error"]["Code"]
        status = 404 if "NonExistent" in code or code.endswith("NotFound") else 502
        return jsonify(error=code, message=e.response["Error"]["Message"]), status

    def body_field(name: str):
        data = request.get_json(silent=True) or {}
        value = data.get(name)
        if not isinstance(value, str) or not value:
            return None
        return value

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.post("/queues")
    def create_queue():
        name = body_field("queue_name")
        if not name:
            return jsonify(error="'queue_name' (string) is required"), 400
        return jsonify(queue_url=service.create_queue(name)), 201

    @app.post("/queues/<name>/messages")
    def send_message(name):
        body = body_field("message_body")
        if not body:
            return jsonify(error="'message_body' (string) is required"), 400
        return jsonify(message_id=service.send_message(name, body)), 201

    @app.post("/queues/<name>/messages/receive")   # POST: receiving deletes the message
    def receive_message(name):
        message = service.receive_message(name)
        if message is None:
            return "", 204
        return jsonify(message=message), 200

    @app.delete("/queues/<name>")
    def delete_queue(name):
        service.delete_queue(name)
        return "", 204

    return app


if __name__ == "__main__":  # development only; use gunicorn in production
    create_app().run(host="127.0.0.1", port=5000)

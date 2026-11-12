import logging
import os
from io import BytesIO
from typing import BinaryIO, Callable, cast

from flask import Flask, jsonify, render_template, request
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge

import face_service
from face_service import FaceVerificationError

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_IMAGE_BYTES = 8 * 1024 * 1024
verify_faces = cast(
    Callable[[BinaryIO, BinaryIO], dict[str, object]], face_service.verify_faces
)


def create_app(test_config: dict[str, object] | None = None):
    app = Flask(__name__)
    app.config.from_mapping(
        MAX_CONTENT_LENGTH=MAX_IMAGE_BYTES * 2 + 1024 * 1024,
        TESTING=False,
    )
    if test_config:
        cast(dict[str, object], app.config).update(test_config)

    logging.basicConfig(level=logging.INFO)

    @app.errorhandler(413)
    def request_too_large(error: RequestEntityTooLarge):
        del error
        return jsonify({"error": "Upload too large. Each image must be 8 MB or smaller."}), 413

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/face_compare")
    def face_compare():
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")

        if file1 is None or file2 is None:
            return jsonify({"error": "Upload both images using fields file1 and file2."}), 400
        image_streams: list[BytesIO] = []
        for uploaded in (file1, file2):
            filename = uploaded.filename
            if not filename:
                return jsonify({"error": "Choose both image files."}), 400
            extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
            if extension not in ALLOWED_EXTENSIONS:
                return jsonify({"error": "Unsupported file extension. Use JPG, PNG, or WEBP."}), 415
            raw = uploaded.read(MAX_IMAGE_BYTES + 1)
            if not raw:
                return jsonify({"error": "An uploaded image is empty."}), 400
            if len(raw) > MAX_IMAGE_BYTES:
                return jsonify({"error": "Each image must be 8 MB or smaller."}), 413
            image_streams.append(BytesIO(raw))

            try:
                with Image.open(BytesIO(raw)) as image:
                    image.verify()
            except (UnidentifiedImageError, OSError, ValueError):
                return jsonify({"error": "One of the files is not a valid image."}), 400

        try:
            result = verify_faces(image_streams[0], image_streams[1])
            return jsonify(result), 200
        except FaceVerificationError as exc:
            return jsonify({"error": str(exc)}), 422
        except Exception:
            app.logger.exception("Unexpected face verification error")
            return jsonify({"error": "Verification could not be completed."}), 500

    return app


app = create_app()

if __name__ == "__main__":
    # Debug is deliberately disabled by default. Set FLASK_DEBUG=1 only locally.
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )

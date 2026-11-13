import io, logging
from typing import Any, Callable, cast

from flask import Flask, render_template, request, jsonify
from PIL import Image
from config import FLASK_HOST, FLASK_PORT, DEBUG, DEFAULT_MODE
from src.predict import Predictor
from src.preprocessing import preprocess_canvas_list, preprocess_pil_image

preprocess_canvas_list = cast(Callable[[Any], Any], preprocess_canvas_list)
preprocess_pil_image = cast(Callable[[Any], Any], preprocess_pil_image)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
predictor = Predictor()

@app.route("/")
def index():
    return render_template("index.html", default_mode=DEFAULT_MODE)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "models_loaded": predictor.loaded_models(), "default_mode": DEFAULT_MODE})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True, silent=True) or {}
        if "image" not in data:
            return jsonify({"error": "Missing 'image' field"}), 400
        mode = data.get("mode", DEFAULT_MODE)
        if mode not in ("combined", "digits", "letters"):
            return jsonify({"error": "mode must be combined|digits|letters"}), 400
        arr = preprocess_canvas_list(data["image"])
        return jsonify(predictor.predict_array(arr, mode=mode))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.exception("Predict failed")
        return jsonify({"error": str(e)}), 500

@app.route("/predict-file", methods=["POST"])
def predict_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        mode = request.form.get("mode", DEFAULT_MODE)
        img = Image.open(io.BytesIO(request.files["file"].read()))
        arr = preprocess_pil_image(img)
        return jsonify(predictor.predict_array(arr, mode=mode))
    except Exception as e:
        logger.exception("File predict failed")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG)

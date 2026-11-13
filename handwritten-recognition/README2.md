# Handwritten Recognition — Digits + Letters

One unified Flask + TensorFlow project that recognizes handwritten digits (0-9) and letters (A-Z) from a drawing canvas or an uploaded image.

## Features

- Single model (36 classes) or two separate models (10 digits + 26 letters)
- Unified preprocessing: grayscale, invert, center, resize to 28x28
- Canvas drawing + image upload
- Top-3 predictions + confidence
- Preprocessing preview (what the model actually sees)
- Training with augmentation, EarlyStopping, Checkpoint, BatchNorm + Dropout
- REST API: `/`, `/predict`, `/health`, `/predict-file`
- Unit tests with pytest

 Project Structure

handwritten-recognition/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── model.py
│   ├── train.py
│   ├── predict.py
│   └── utils/helpers.py
├── scripts/
│   ├── train_digits.py
│   ├── train_letters.py
│   └── train_combined.py
├── templates/index.html
├── static/css/style.css
├── static/js/app.js
├── tests/
└── model/

Quick Start

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/train_combined.py --epochs 12
python app.py

Open http://127.0.0.1:5000
pytest -v

API
POST /predict -> {"image": [...], "mode": "combined"}
POST /predict-file -> form file=image
GET /health

Fixes vs Original Code

- EMNIST labels 1-26 -> 0-25
- EMNIST images transposed back
- x_test normalized
- EMNIST via tensorflow_datasets
- Unified inversion / centering
- .keras format instead of legacy .h5

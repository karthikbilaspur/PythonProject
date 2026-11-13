import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
COMBINED_MODEL_PATH = MODEL_DIR / "combined_model.keras"
DIGIT_MODEL_PATH = MODEL_DIR / "digit_model.keras"
LETTER_MODEL_PATH = MODEL_DIR / "letter_model.keras"
DEFAULT_MODE = os.getenv("RECOGNITION_MODE", "combined")
CANVAS_SIZE = 280
MODEL_INPUT_SIZE = 28
EPOCHS = 12
BATCH_SIZE = 128
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"
DIGIT_LABELS = [str(i) for i in range(10)]
LETTER_LABELS = [chr(65 + i) for i in range(26)]
COMBINED_LABELS = DIGIT_LABELS + LETTER_LABELS

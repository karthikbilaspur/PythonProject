# FaceVision — Face Verification Web App

A medium-scope portfolio project using Flask, OpenCV, and DeepFace. Users upload two images and receive a model-based face-verification result.

> **Responsible use:** Only process images with appropriate permission. A model result is not proof of identity and can be wrong. Do not use this demo as the sole basis for access, employment, financial, or other high-impact decisions.

## Features

- Simple responsive browser interface with image previews
- Flask REST endpoint for comparing two images
- Image extension, content, and size validation
- DeepFace with FaceNet embeddings and OpenCV face detection
- Clear errors for missing/invalid images and failed verification
- Unit tests for routes, validation, and image decoding
- No intentional persistence of uploaded images

## Project structure

```text
verifyvision/
├── app.py
├── face_service.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── tests/
│   ├── test_app.py
│   └── test_face_service.py
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or a version supported by the installed TensorFlow/DeepFace release
- `pip`
- Internet access on first run if DeepFace needs to download model weights

Deep-learning dependencies can be platform-sensitive. If installation fails, create a clean virtual environment and consult the current DeepFace/TensorFlow installation instructions for your OS and Python version.

## Setup

### 1. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser. The first verification may take longer while the model is initialized or downloaded.

For local debugging only, set `FLASK_DEBUG=1`. Keep debug mode disabled in any shared or production environment.

## API

### `GET /health`

Example response:

```json
{"status": "ok"}
```

### `POST /face_compare`

Send multipart form data containing two image fields named `file1` and `file2`.

Example using curl:

```bash
curl -X POST http://127.0.0.1:5000/face_compare \
  -F "file1=@person_a.jpg" \
  -F "file2=@person_b.jpg"
```

A successful response resembles:

```json
{
  "verified": true,
  "distance": 0.25,
  "threshold": 0.4,
  "message": "Face match",
  "note": "Distance and threshold are model-specific, not identity probabilities."
}
```

The values above are illustrative, not a promise of actual model output. DeepFace's verification threshold and distance depend on the model and configuration. The distance must not be described as a probability.

## Run unit tests

The tests mock the model call where appropriate, so most tests do not need to download face-model weights.

```bash
python -m unittest discover -s tests -v
```

## Important implementation notes

- The model input is decoded into an RGB NumPy array before passing it to DeepFace.
- Face detection can fail for blurry, small, angled, or occluded faces.
- The demo uses the first suitable face pair selected by the verification library. For multi-face images, a production version should define explicit face-selection behavior.
- Upload size is limited; do not remove limits without adding stronger resource controls.
- Uploaded images are not saved by this app, but production hosting, proxies, error monitoring, and temporary storage must also be configured not to retain sensitive content.
- The current app does not include login, Firebase history, rate limiting, or production deployment. Add those only if required, with consent, access controls, and retention policies.

## Security before deployment

- Use a production WSGI server; do not expose Flask's development server.
- Set HTTPS, request limits, rate limits, and timeouts.
- Keep debug mode off.
- Add authentication and authorization if the app is used by multiple users.
- Avoid logging image contents or sensitive biometric data.
- Do not accept arbitrary remote image URLs without strict SSRF protections.

## Resume description

**VerifyVision — Face Verification Web App**  
Built a Flask-based computer-vision application using OpenCV and a pretrained DeepFace model to compare two consented images. Implemented image validation, REST endpoints, responsive UI, error handling, and automated unit tests.

Add measured evaluation results only after testing on a suitable dataset.

## License

Choose and add a license before publishing this repository publicly.

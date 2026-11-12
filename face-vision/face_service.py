"""Face-verification service.

DeepFace's public API accepts image arrays in supported versions. This module
decodes validated image streams with Pillow/NumPy and compares face embeddings.
The returned distance is model-specific; it is not a probability of identity.
"""
from importlib import import_module
from typing import BinaryIO, Protocol, TypedDict, cast

import numpy as np
from numpy.typing import NDArray
from PIL import Image, UnidentifiedImageError


class FaceVerificationError(Exception):
    """Raised when verification cannot be performed safely."""


class _VerificationResult(TypedDict):
    verified: bool
    distance: float
    threshold: float


class _DeepFaceAPI(Protocol):
    def verify(
        self,
        *,
        img1_path: NDArray[np.uint8],
        img2_path: NDArray[np.uint8],
        model_name: str,
        detector_backend: str,
        enforce_detection: bool,
    ) -> _VerificationResult: ...


def _decode_image(stream: BinaryIO):
    try:
        stream.seek(0)
        with Image.open(stream) as image:
            image = image.convert("RGB")
            # Prevent unexpectedly huge decoded images from consuming memory.
            if image.width > 6000 or image.height > 6000:
                raise FaceVerificationError("Image dimensions must not exceed 6000 × 6000.")
            return np.asarray(image)
    except FaceVerificationError:
        raise
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise FaceVerificationError("Could not decode one of the images.") from exc


def verify_faces(image1_stream: BinaryIO, image2_stream: BinaryIO) -> dict[str, bool | float | str]:
    """Verify two images with DeepFace and return a JSON-serializable result."""
    image1 = _decode_image(image1_stream)
    image2 = _decode_image(image2_stream)

    try:
        deepface_module = import_module("deepface")
        deepface = cast(_DeepFaceAPI, getattr(deepface_module, "DeepFace"))
    except ImportError as exc:
        raise FaceVerificationError(
            "DeepFace is not installed. Install dependencies from requirements.txt."
        ) from exc

    try:
        result = deepface.verify(
            img1_path=image1,
            img2_path=image2,
            model_name="Facenet",
            detector_backend="opencv",
            enforce_detection=True,
        )
    except ValueError as exc:
        # DeepFace commonly raises ValueError when a face cannot be detected.
        raise FaceVerificationError(
            "Could not detect a face in both images. Try clearer, front-facing photos."
        ) from exc
    except Exception as exc:
        # Avoid leaking internal errors or image data to the client.
        raise FaceVerificationError(
            "The face-verification model failed. Check model installation and try again."
        ) from exc

    return {
        "verified": bool(result["verified"]),
        "distance": float(result["distance"]),
        "threshold": float(result["threshold"]),
        "message": "Face match" if result["verified"] else "No match detected",
        "note": "Distance and threshold are model-specific, not identity probabilities.",
    }

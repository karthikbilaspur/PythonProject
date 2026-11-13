import numpy as np
from numpy.typing import ArrayLike, NDArray
from PIL import Image
import cv2
CANVAS_SIZE = 280
TARGET = 28
def _center_and_resize(gray: NDArray[np.uint8]) -> NDArray[np.uint8]:
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    if cv2.countNonZero(thresh) == 0:
        return np.zeros((TARGET, TARGET), dtype=np.uint8)
    coords = cv2.findNonZero(thresh)
    x, y, w, h = cv2.boundingRect(coords)
    roi = gray[y:y+h, x:x+w]
    size = max(w, h)
    padded = np.zeros((size, size), dtype=np.uint8)
    padded[(size-h)//2:(size-h)//2+h, (size-w)//2:(size-w)//2+w] = roi
    resized = cv2.resize(padded, (20, 20), interpolation=cv2.INTER_AREA)
    canvas = np.zeros((TARGET, TARGET), dtype=np.uint8)
    canvas[4:24, 4:24] = resized
    return canvas
def preprocess_canvas_list(image_data: ArrayLike):
    arr = np.array(image_data, dtype=np.float32)
    if arr.size == CANVAS_SIZE*CANVAS_SIZE:
        arr = arr.reshape((CANVAS_SIZE, CANVAS_SIZE))
    elif arr.size == TARGET*TARGET:
        arr = arr.reshape((TARGET, TARGET))
    else:
        raise ValueError(f"Expected {CANVAS_SIZE*CANVAS_SIZE} or {TARGET*TARGET} pixels, got {arr.size}")
    if arr.mean() > 127:
        arr = 255 - arr
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    centered = _center_and_resize(arr)
    return (centered.astype(np.float32)/255.0).reshape((1, TARGET, TARGET, 1))
def preprocess_pil_image(img: Image.Image):
    gray = img.convert("L")
    gray.thumbnail((CANVAS_SIZE, CANVAS_SIZE), Image.Resampling.LANCZOS)
    arr: NDArray[np.uint8] = np.asarray(gray, dtype=np.uint8)
    border = np.concatenate([arr[0,:], arr[-1,:], arr[:,0], arr[:,-1]], out=None)
    if np.median(border) > 127:
        arr = 255 - arr
    centered = _center_and_resize(arr.astype(np.uint8))
    return (centered.astype(np.float32)/255.0).reshape((1, TARGET, TARGET, 1))
def preprocess_for_training(x: NDArray[np.uint8]) -> NDArray[np.float32]:
    return (x.astype(np.float32) / 255.0)[..., np.newaxis]

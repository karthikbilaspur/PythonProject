import pytest
import cv2
import numpy as np
import os
import tempfile
from utils.photo_processor import is_good_photo

def test_no_face_image():
    # Create blank image (no face)
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        blank = np.zeros((200,200,3), dtype=np.uint8)
        cv2.imwrite(tmp.name, blank)
        result = is_good_photo(tmp.name)
        assert result['has_face'] == False
        os.unlink(tmp.name)

def test_invalid_path():
    result = is_good_photo('/nonexistent/path.jpg')
    assert result['has_face'] == False

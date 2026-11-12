import io
import unittest

import numpy as np
from PIL import Image

from face_service import _decode_image, FaceVerificationError


class FaceServiceUnitTests(unittest.TestCase):
    def test_decodes_rgb_image(self):
        stream = io.BytesIO()
        Image.new("RGB", (12, 8), (1, 2, 3)).save(stream, format="PNG")
        stream.seek(0)
        result = _decode_image(stream)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (8, 12, 3))
        self.assertEqual(result.dtype, np.uint8)

    def test_invalid_image_raises_clear_error(self):
        with self.assertRaises(FaceVerificationError):
            _decode_image(io.BytesIO(b"not an image"))


if __name__ == "__main__":
    unittest.main()

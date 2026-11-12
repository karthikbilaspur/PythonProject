import io
import unittest
from unittest.mock import patch

from PIL import Image

from app import create_app


def image_bytes(fmt="JPEG", color=(80, 120, 160)):
    stream = io.BytesIO()
    Image.new("RGB", (32, 32), color).save(stream, format=fmt)
    return stream.getvalue()


class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True})
        self.client = self.app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"VerifyVision", response.data)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_requires_both_files(self):
        response = self.client.post("/face_compare", data={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Upload both images", response.get_json()["error"])

    def test_rejects_unsupported_extension(self):
        response = self.client.post(
            "/face_compare",
            data={
                "file1": (io.BytesIO(b"file"), "one.gif"),
                "file2": (io.BytesIO(b"file"), "two.jpg"),
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 415)

    def test_rejects_invalid_image(self):
        response = self.client.post(
            "/face_compare",
            data={
                "file1": (io.BytesIO(b"not an image"), "one.jpg"),
                "file2": (io.BytesIO(image_bytes()), "two.jpg"),
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)

    @patch("app.verify_faces")
    def test_successful_verification(self, mock_verify):
        mock_verify.return_value = {
            "verified": True,
            "distance": 0.25,
            "threshold": 0.4,
            "message": "Face match",
            "note": "Model-specific distance.",
        }
        response = self.client.post(
            "/face_compare",
            data={
                "file1": (io.BytesIO(image_bytes()), "one.jpg"),
                "file2": (io.BytesIO(image_bytes(color=(20, 40, 60))), "two.jpg"),
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["verified"])
        mock_verify.assert_called_once()

    @patch("app.verify_faces")
    def test_face_not_detected(self, mock_verify):
        from face_service import FaceVerificationError
        mock_verify.side_effect = FaceVerificationError("No face detected.")
        response = self.client.post(
            "/face_compare",
            data={
                "file1": (io.BytesIO(image_bytes()), "one.jpg"),
                "file2": (io.BytesIO(image_bytes()), "two.jpg"),
            },
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("No face detected", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()

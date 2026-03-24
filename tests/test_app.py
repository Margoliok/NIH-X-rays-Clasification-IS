import base64
import io
import tempfile
import unittest
from pathlib import Path

from medvision import create_app
from medvision.extensions import db
from medvision.models import AnalysisRecord


PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9sWzx2QAAAAASUVORK5CYII="
)


class MedVisionAppTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        upload_dir = Path(self.temp_dir.name) / "uploads"
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "UPLOAD_FOLDER": str(upload_dir),
                "PREDICTOR_MODE": "demo",
                "SECRET_KEY": "test-secret",
            }
        )
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.temp_dir.cleanup()

    def test_core_pages_render(self):
        for path in ("/", "/analyze", "/diseases", "/history"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)

    def test_language_switch_to_russian(self):
        response = self.client.get("/language/ru?next=/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Главная".encode("utf-8"), response.data)

    def test_upload_creates_history_record(self):
        response = self.client.post(
            "/analyze",
            data={"xray_image": (io.BytesIO(PNG_BYTES), "healthy-sample.png")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        with self.app.app_context():
            records = AnalysisRecord.query.all()
            self.assertEqual(len(records), 1)
            self.assertEqual(len(records[0].top_predictions), 3)

    def test_invalid_extension_is_rejected(self):
        response = self.client.post(
            "/analyze",
            data={"xray_image": (io.BytesIO(b"not-an-image"), "bad.txt")},
            content_type="multipart/form-data",
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            self.assertEqual(AnalysisRecord.query.count(), 0)


if __name__ == "__main__":
    unittest.main()

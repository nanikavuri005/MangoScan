from io import BytesIO
from fastapi.testclient import TestClient
from PIL import Image

from main import app

client = TestClient(app)


def build_image_bytes(color=(20, 160, 20)):
    img = Image.new("RGB", (12, 12), color)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_accepts_image():
    data = build_image_bytes()
    response = client.post(
        "/analyze",
        files={"image": ("leaf.png", data, "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert "diagnosis" in body
    assert "confidence" in body


def test_analyze_rejects_non_image_content_type():
    response = client.post(
        "/analyze",
        files={"image": ("file.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400

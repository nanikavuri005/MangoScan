from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image

from disease_practices import normalize_disease_name
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
    body = response.json()
    assert body["status"] == "ok"
    assert "model_loaded" in body
    assert "min_confidence" in body


def test_analyze_accepts_image_and_returns_structured_output():
    data = build_image_bytes()
    response = client.post(
        "/analyze",
        files={"image": ("leaf.png", data, "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert "diagnosis" in body
    assert "rawPrediction" in body
    assert "confidence" in body
    assert "topPredictions" in body
    assert isinstance(body["topPredictions"], list)
    assert "practices" in body
    assert isinstance(body["practices"], list)


def test_normalize_disease_name_handles_aliases():
    assert normalize_disease_name("powdery_mildew") == "Powdery Mildew"
    assert normalize_disease_name("sooty mold") == "Sooty Mould"


def test_analyze_rejects_non_image_content_type():
    response = client.post(
        "/analyze",
        files={"image": ("file.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400

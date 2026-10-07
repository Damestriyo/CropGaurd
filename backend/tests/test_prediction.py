import io
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def create_test_image(format: str = "JPEG", size=(256, 256), color=(34, 139, 34)) -> io.BytesIO:
    """Helper to generate an in-memory test image."""
    buffer = io.BytesIO()
    mode = "RGB" if format.upper() in ("JPEG", "JPG") else "RGBA"
    image = Image.new(mode, size, color=color)
    image.save(buffer, format=format)
    buffer.seek(0)
    return buffer


def test_root_endpoint():
    """Verify root status check."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "project" in data
    assert "database" in data


def test_health_endpoint():
    """Verify health check."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data


def test_valid_jpeg_prediction():
    """Verify valid JPEG upload returns complete diagnosis and disease management."""
    img_buffer = create_test_image("JPEG", size=(300, 200))
    files = {"file": ("leaf.jpg", img_buffer, "image/jpeg")}

    response = client.post("/predict", files=files)
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["id"] is not None
    # Verify metadata
    meta = data["image_metadata"]
    assert meta["filename"] == "leaf.jpg"
    assert meta["width"] == 300
    assert meta["height"] == 200
    assert meta["format"] == "JPEG"

    # Verify prediction output (Phase 5)
    pred = data["prediction"]
    assert pred["crop"] == "Tomato"
    assert pred["disease"] == "Early Blight"
    assert pred["confidence"] == 94.62
    assert pred["severity"] == "Moderate"
    assert pred["is_healthy"] is False

    # Verify enriched clinical info (Phase 9)
    info = data["disease_info"]
    assert info is not None
    assert info["id"] == "tomato-early-blight"
    assert len(info["symptoms"]) > 0
    assert len(info["causes"]) > 0
    assert len(info["prevention"]) > 0
    assert len(info["management"]) > 0


def test_valid_png_prediction():
    """Verify valid PNG upload processes properly."""
    img_buffer = create_test_image("PNG", size=(128, 128))
    files = {"file": ("healthy_leaf.png", img_buffer, "image/png")}

    response = client.post("/predict", files=files)
    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["image_metadata"]["format"] == "PNG"
    assert "prediction" in data


def test_both_routes_work_without_redirect():
    """Verify both /predict and /predict/ respond with 200 without 307 redirect."""
    img_buffer1 = create_test_image("JPEG")
    res1 = client.post("/predict", files={"file": ("leaf1.jpg", img_buffer1, "image/jpeg")})
    assert res1.status_code == 200

    img_buffer2 = create_test_image("JPEG")
    res2 = client.post("/predict/", files={"file": ("leaf2.jpg", img_buffer2, "image/jpeg")})
    assert res2.status_code == 200


def test_invalid_extension():
    """Verify unsupported file extension returns 415."""
    fake_doc = io.BytesIO(b"Dummy PDF content")
    files = {"file": ("document.pdf", fake_doc, "application/pdf")}

    response = client.post("/predict", files=files)
    assert response.status_code == 415
    assert "Unsupported file extension" in response.json()["detail"]


def test_invalid_mime_type():
    """Verify disallowed MIME type returns 415."""
    img_buffer = create_test_image("JPEG")
    files = {"file": ("leaf.jpg", img_buffer, "text/plain")}

    response = client.post("/predict", files=files)
    assert response.status_code == 415
    assert "Unsupported MIME type" in response.json()["detail"]


def test_corrupt_image_payload():
    """Verify non-image bytes disguised as image return 400."""
    fake_img = io.BytesIO(b"THIS_IS_DEFINITELY_NOT_AN_IMAGE_FILE")
    files = {"file": ("fake_leaf.jpg", fake_img, "image/jpeg")}

    response = client.post("/predict", files=files)
    assert response.status_code == 400
    assert "Invalid or corrupted image" in response.json()["detail"]


def test_empty_file_upload():
    """Verify empty file (0 bytes) returns 400."""
    empty_file = io.BytesIO(b"")
    files = {"file": ("empty.jpg", empty_file, "image/jpeg")}

    response = client.post("/predict", files=files)
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

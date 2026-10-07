import io
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def create_test_image(format: str = "JPEG", size=(200, 200), color=(50, 150, 50)) -> io.BytesIO:
    """Helper to generate an in-memory test image."""
    buffer = io.BytesIO()
    image = Image.new("RGB", size, color=color)
    image.save(buffer, format=format)
    buffer.seek(0)
    return buffer


def test_list_history_returns_200():
    """Verify history listing returns valid status and list structure."""
    response = client.get("/history")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)


def test_prediction_creates_and_retrieves_history_record():
    """Verify that performing a prediction persists a record queryable via /history."""
    img_buffer = create_test_image("JPEG", size=(250, 250))
    files = {"file": ("corn_leaf.jpg", img_buffer, "image/jpeg")}

    # 1. Perform prediction
    pred_res = client.post("/predict", files=files)
    assert pred_res.status_code == 200
    pred_data = pred_res.json()
    record_id = pred_data.get("id")
    assert record_id is not None

    # 2. Retrieve scan record by ID
    hist_res = client.get(f"/history/{record_id}")
    assert hist_res.status_code == 200
    hist_data = hist_res.json()

    assert hist_data["id"] == record_id
    assert hist_data["filename"] == "corn_leaf.jpg"
    assert hist_data["crop"] == pred_data["prediction"]["crop"]
    assert hist_data["disease"] == pred_data["prediction"]["disease"]
    assert hist_data["confidence"] == pred_data["prediction"]["confidence"]
    assert "image_metadata" in hist_data


def test_get_nonexistent_history_record():
    """Verify 404 for unknown history ID."""
    response = client.get("/history/invalid_record_id_12345")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_history_record():
    """Verify deleting a prediction record from history."""
    img_buffer = create_test_image("JPEG")
    files = {"file": ("to_delete.jpg", img_buffer, "image/jpeg")}

    # Create record
    pred_res = client.post("/predict", files=files)
    record_id = pred_res.json()["id"]

    # Delete record
    del_res = client.delete(f"/history/{record_id}")
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Confirm it is no longer found
    get_res = client.get(f"/history/{record_id}")
    assert get_res.status_code == 404

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_all_diseases():
    """Verify listing all documented diseases."""
    response = client.get("/diseases")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 8
    assert len(data["diseases"]) >= 8


def test_filter_diseases_by_crop():
    """Verify filtering diseases by specific crop."""
    response = client.get("/diseases?crop=Tomato")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 3
    for disease in data["diseases"]:
        assert disease["crop"].lower() == "tomato"


def test_get_existing_disease_by_id():
    """Verify retrieving detailed disease clinical guide by ID."""
    response = client.get("/diseases/tomato-early-blight")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == "tomato-early-blight"
    assert data["crop"] == "Tomato"
    assert data["disease"] == "Early Blight"
    assert data["scientific_name"] == "Alternaria solani"
    assert data["severity"] == "Moderate"
    assert isinstance(data["symptoms"], list)
    assert len(data["symptoms"]) > 0
    assert isinstance(data["management"], list)
    assert len(data["management"]) > 0


def test_get_nonexistent_disease():
    """Verify 404 response for unknown disease ID."""
    response = client.get("/diseases/unknown-alien-disease")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

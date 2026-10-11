import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.disease import DiseaseBase
from app.services.disease_service import DiseaseService
from app.services.predictor import CLASS_MAPPING

client = TestClient(app)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
with (REPOSITORY_ROOT / "ml" / "artifacts" / "class_names.json").open(encoding="utf-8") as class_file:
    MODEL_CLASS_NAMES = json.load(class_file)

EXPECTED_CATALOG_IDS = {
    "Pepper__bell___Bacterial_spot": "pepper-bacterial-spot",
    "Pepper__bell___healthy": "pepper-healthy",
    "Potato___Early_blight": "potato-early-blight",
    "Potato___Late_blight": "potato-late-blight",
    "Potato___healthy": "potato-healthy",
    "Tomato_Bacterial_spot": "tomato-bacterial-spot",
    "Tomato_Early_blight": "tomato-early-blight",
    "Tomato_Late_blight": "tomato-late-blight",
    "Tomato_Leaf_Mold": "tomato-leaf-mold",
    "Tomato_Septoria_leaf_spot": "tomato-septoria-leaf-spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite": "tomato-spider-mites",
    "Tomato__Target_Spot": "tomato-target-spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus": "tomato-yellow-leaf-curl-virus",
    "Tomato__Tomato_mosaic_virus": "tomato-mosaic-virus",
    "Tomato_healthy": "tomato-healthy",
}


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


def test_tomato_leaf_mold_prediction_lookup_is_case_insensitive():
    disease = DiseaseService.get_info_for_prediction("tomato", "leaf mold")
    assert isinstance(disease, DiseaseBase)
    assert disease.id == "tomato-leaf-mold"
    assert disease.crop == "Tomato"
    assert disease.disease == "Leaf Mold"
    assert disease.scientific_name == "Passalora fulva"
    assert disease.is_healthy is False
    assert disease.severity == "Moderate"
    assert disease.symptoms and disease.causes and disease.prevention and disease.management


def test_unlisted_prediction_still_has_no_catalog_entry():
    assert DiseaseService.get_info_for_prediction("Tomato", "Unlisted Disease") is None


def test_class_names_file_is_fully_covered_by_expected_catalog_ids():
    assert len(MODEL_CLASS_NAMES) == 15
    assert set(MODEL_CLASS_NAMES) == set(EXPECTED_CATALOG_IDS)
    assert set(MODEL_CLASS_NAMES).issubset(CLASS_MAPPING)


@pytest.mark.parametrize("model_class", MODEL_CLASS_NAMES)
def test_each_model_class_resolves_to_its_catalog_entry(model_class):
    crop, disease_name, is_healthy = CLASS_MAPPING[model_class]
    # Exercise canonical names with mixed case/separators and the raw class
    # name with its crop prefix/cultivar tokens.
    catalog_entry = DiseaseService.get_info_for_prediction(
        crop.lower(), disease_name.lower().replace(" ", "_")
    )
    raw_label_entry = DiseaseService.get_info_for_prediction(crop, model_class)
    assert catalog_entry is not None, model_class
    assert raw_label_entry is not None, model_class
    assert catalog_entry.id == EXPECTED_CATALOG_IDS[model_class]
    assert raw_label_entry.id == EXPECTED_CATALOG_IDS[model_class]
    assert catalog_entry.crop == crop
    assert catalog_entry.is_healthy is is_healthy
    if is_healthy:
        assert catalog_entry.disease == "Healthy"
        assert catalog_entry.severity == "None"
    else:
        assert catalog_entry.scientific_name
        assert catalog_entry.severity in {"Low", "Moderate", "High", "Critical"}
        assert catalog_entry.symptoms and catalog_entry.causes
        assert catalog_entry.prevention and catalog_entry.management

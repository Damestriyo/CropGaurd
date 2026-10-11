import pytest

from app.services.predictor import CLASS_MAPPING, PredictorService


class MockPlantPredictor:
    class_names = list(CLASS_MAPPING)

    def __init__(self):
        self.result = {
            "predicted_class": "Tomato_Early_blight",
            "confidence": 0.9462,
            "top_predictions": [],
        }
        self.calls = 0

    def predict(self, image_path, top_k=3):
        self.calls += 1
        return self.result


@pytest.fixture(autouse=True)
def mock_model(monkeypatch):
    model = MockPlantPredictor()
    monkeypatch.setattr(PredictorService, "_model", model)
    monkeypatch.setattr(PredictorService, "_class_labels", list(CLASS_MAPPING))
    yield model
    monkeypatch.setattr(PredictorService, "_model", None)
    monkeypatch.setattr(PredictorService, "_class_labels", [])

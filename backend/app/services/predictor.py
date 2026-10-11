"""MobileNetV2 inference and API response mapping."""

import importlib.util
import io
import logging
from pathlib import Path
from typing import Dict, Tuple

from fastapi import HTTPException
from PIL import Image

from app.schemas.prediction import PredictionResult
from app.services.disease_service import DiseaseService

logger = logging.getLogger(__name__)

# Names are the exact labels emitted by ml/artifacts/class_names.json.
CLASS_MAPPING: Dict[str, Tuple[str, str, bool]] = {
    "Pepper__bell___Bacterial_spot": ("Pepper", "Bacterial Spot", False),
    "Pepper__bell___healthy": ("Pepper", "Healthy", True),
    "Potato___Early_blight": ("Potato", "Early Blight", False),
    "Potato___Late_blight": ("Potato", "Late Blight", False),
    "Potato___healthy": ("Potato", "Healthy", True),
    "Tomato_Bacterial_spot": ("Tomato", "Bacterial Spot", False),
    "Tomato_Early_blight": ("Tomato", "Early Blight", False),
    "Tomato_Late_blight": ("Tomato", "Late Blight", False),
    "Tomato_Leaf_Mold": ("Tomato", "Leaf Mold", False),
    "Tomato_Septoria_leaf_spot": ("Tomato", "Septoria Leaf Spot", False),
    "Tomato_Spider_mites_Two_spotted_spider_mite": ("Tomato", "Spider Mites", False),
    "Tomato__Target_Spot": ("Tomato", "Target Spot", False),
    "Tomato__Tomato_YellowLeaf__Curl_Virus": ("Tomato", "Yellow Leaf Curl Virus", False),
    "Tomato__Tomato_mosaic_virus": ("Tomato", "Mosaic Virus", False),
    "Tomato_healthy": ("Tomato", "Healthy", True),
}


class PredictorService:
    """Loads one trained predictor at application startup and reuses it per request."""

    _model = None
    _class_labels = []

    @classmethod
    def load_model(cls, artifacts_dir: str = None):
        """Load and validate the existing ML predictor from repository artifacts."""
        root = Path(__file__).resolve().parents[3]
        cls._model = None
        cls._class_labels = []
        artifact_path = Path(artifacts_dir) if artifacts_dir else root / "ml" / "artifacts"
        if not artifact_path.is_absolute():
            artifact_path = root / artifact_path
        artifact_path = artifact_path.resolve()
        predictor_path = root / "ml" / "src" / "predict.py"
        required = [artifact_path / name for name in (
            "mobilenetv2_best.pth", "class_names.json", "preprocessing.json"
        )]
        missing = [str(path) for path in required if not path.is_file()]
        if missing:
            raise RuntimeError("MobileNetV2 model artifacts are missing: " + ", ".join(missing))
        if not predictor_path.is_file():
            raise RuntimeError(f"MobileNetV2 predictor implementation not found: {predictor_path}")

        try:
            spec = importlib.util.spec_from_file_location("cropguard_ml_predict", predictor_path)
            if spec is None or spec.loader is None:
                raise RuntimeError(f"Could not load predictor module: {predictor_path}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            model = module.PlantDiseasePredictor(artifact_path)
            labels = list(model.class_names)
            unmapped = set(labels) - set(CLASS_MAPPING)
            missing_labels = set(CLASS_MAPPING) - set(labels)
            if unmapped or missing_labels:
                raise ValueError(
                    f"Model labels do not match API mapping (unmapped={sorted(unmapped)}, "
                    f"not_in_model={sorted(missing_labels)})"
                )
        except Exception as exc:
            cls._model = None
            cls._class_labels = []
            raise RuntimeError(f"Failed to initialize MobileNetV2 model from {artifact_path}: {exc}") from exc

        cls._model = model
        cls._class_labels = labels
        logger.info("Loaded MobileNetV2 predictor with %d classes from %s", len(labels), artifact_path)
        return model

    @classmethod
    def predict(cls, image: Image.Image) -> PredictionResult:
        if cls._model is None:
            raise RuntimeError("MobileNetV2 predictor has not been loaded during application startup.")
        try:
            # The existing predictor accepts a file-like object through Pillow's Image.open.
            buffer = io.BytesIO()
            image.convert("RGB").save(buffer, format="PNG")
            buffer.seek(0)
            result = cls._model.predict(buffer, top_k=1)
            label = result["predicted_class"]
            crop, disease, healthy = CLASS_MAPPING[label]
            probability = float(result["confidence"])
            if not 0.0 <= probability <= 1.0:
                raise ValueError(f"Model returned invalid probability: {probability}")
        except Exception as exc:
            logger.exception("MobileNetV2 inference failed")
            raise HTTPException(status_code=503, detail="Crop disease inference is temporarily unavailable.") from exc

        return PredictionResult(
            crop=crop,
            disease=disease,
            confidence=round(probability * 100.0, 2),
            # Image classification does not estimate severity; keep this neutral.
            severity="None" if healthy else "Unknown",
            is_healthy=healthy,
        )

    @classmethod
    def diagnose_and_enrich(cls, image: Image.Image):
        """Run classification and attach catalog information when available."""
        prediction = cls.predict(image)
        disease_info = DiseaseService.get_info_for_prediction(
            crop=prediction.crop,
            disease=prediction.disease,
        )
        return prediction, disease_info

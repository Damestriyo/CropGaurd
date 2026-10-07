import logging
from PIL import Image

from app.schemas.prediction import PredictionResult
from app.services.disease_service import DiseaseService

logger = logging.getLogger(__name__)


class PredictorService:
    """
    Inference service for crop disease classification.
    
    When a trained deep learning model is provided by the Deep Learning teammate,
    it is loaded once here and executes real tensor inference.
    
    In the interim (prior to model handoff), this service returns a contract-compliant
    simulation to enable the Frontend developer to build and test UI/UX flows.
    """

    _model = None
    _class_labels = []

    @classmethod
    def load_model(cls, model_path: str = None):
        """
        Loads the deep learning model into memory once at startup.
        To be implemented when the Deep Learning teammate delivers the model artifact.
        """
        logger.info("PredictorService: Running in development mode awaiting ML model artifact.")
        cls._model = None

    @classmethod
    def predict(cls, image: Image.Image) -> PredictionResult:
        """
        Performs disease diagnosis on a PIL Image.
        Returns a strongly-typed PredictionResult.
        """
        if cls._model is not None:
            # Placeholder for actual model inference once DL model is loaded
            raise NotImplementedError("Real ML model inference logic will run here.")

        # Contract Simulation Mode for Frontend Team Integration:
        # Generate a realistic crop disease diagnosis based on our knowledge catalog
        return PredictionResult(
            crop="Tomato",
            disease="Early Blight",
            confidence=94.62,
            severity="Moderate",
            is_healthy=False
        )

    @classmethod
    def diagnose_and_enrich(cls, image: Image.Image):
        """
        Runs prediction and attaches clinical disease management information.
        """
        prediction = cls.predict(image)
        disease_info = DiseaseService.get_info_for_prediction(
            crop=prediction.crop,
            disease=prediction.disease
        )
        return prediction, disease_info

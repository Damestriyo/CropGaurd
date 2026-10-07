from fastapi import APIRouter, UploadFile, File, status

from app.services.image_processor import ImageProcessorService
from app.services.predictor import PredictorService
from app.services.history_service import HistoryService
from app.schemas.prediction import FullPredictionResponse, APIErrorResponse

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post(
    "",
    response_model=FullPredictionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": APIErrorResponse, "description": "Invalid or corrupted image"},
        413: {"model": APIErrorResponse, "description": "Payload exceeds maximum allowed size"},
        415: {"model": APIErrorResponse, "description": "Unsupported media type or extension"},
    },
    summary="Analyze leaf image and detect crop disease",
    description="Validates image upload, runs disease classification inference, attaches structured guidance, and saves record to database (Phase 6)."
)
@router.post(
    "/",
    response_model=FullPredictionResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def predict_crop_disease(file: UploadFile = File(...)):
    """
    Primary endpoint for leaf image diagnosis.

    - **file**: Multipart form image upload (JPEG, PNG, or WEBP).
    """
    # 1. Validate file format, MIME type, and size thresholds
    contents = await ImageProcessorService.read_and_validate_file(file)

    # 2. Inspect image integrity and extract metadata
    image, metadata = ImageProcessorService.inspect_and_verify_image(
        contents=contents,
        filename=file.filename,
        content_type=file.content_type
    )

    # 3. Perform prediction diagnosis and enrich with disease knowledge
    prediction, disease_info = PredictorService.diagnose_and_enrich(image)

    # 4. Persist scan record into database (Phase 6)
    saved_record = await HistoryService.record_prediction(
        filename=file.filename,
        image_metadata=metadata,
        prediction=prediction,
        user_id=None
    )

    return FullPredictionResponse(
        id=saved_record.id,
        success=True,
        message="Crop disease detection completed successfully.",
        image_metadata=metadata,
        prediction=prediction,
        disease_info=disease_info
    )
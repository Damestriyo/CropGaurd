from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.disease import DiseaseBase


class ImageMetadata(BaseModel):
    """Extracted metadata of an uploaded and validated image."""
    filename: str = Field(..., description="Original name of the uploaded file")
    content_type: str = Field(..., description="MIME type detected for the file")
    size_bytes: int = Field(..., description="File size in bytes")
    size_kb: float = Field(..., description="File size in kilobytes")
    width: int = Field(..., description="Width of the image in pixels")
    height: int = Field(..., description="Height of the image in pixels")
    format: str = Field(..., description="Image format (e.g. JPEG, PNG, WEBP)")
    mode: str = Field(..., description="Color mode (e.g. RGB, RGBA, L)")
    channels: int = Field(..., description="Number of color channels")


class PredictionResult(BaseModel):
    """Inference classification result returned by model."""
    crop: str = Field(..., description="Identified plant or crop species")
    disease: str = Field(..., description="Diagnosed condition or 'Healthy'")
    confidence: float = Field(..., description="Prediction confidence score percentage (0-100)")
    severity: str = Field(..., description="Disease severity level (Low, Moderate, High, None)")
    is_healthy: bool = Field(False, description="Whether the leaf is diagnosed healthy")


class FullPredictionResponse(BaseModel):
    """Complete prediction response returned to frontend client (Phase 5 & 6)."""
    id: Optional[str] = Field(None, description="Unique prediction scan ID recorded in database")
    success: bool = Field(True, description="Status indicating prediction success")
    message: str = Field(..., description="Human-readable status summary")
    image_metadata: ImageMetadata = Field(..., description="Verified image characteristics")
    prediction: PredictionResult = Field(..., description="Disease classification output")
    disease_info: Optional[DiseaseBase] = Field(None, description="Detailed symptoms and treatment guidance")


class ImageUploadValidationResponse(BaseModel):
    """Response returned upon validation-only request (Phase 2 legacy support)."""
    success: bool = Field(True, description="Status indicating validation success")
    message: str = Field(..., description="Human-readable status message")
    image_metadata: ImageMetadata = Field(..., description="Verified image properties")


class APIErrorResponse(BaseModel):
    """Standardized error response schema."""
    success: bool = Field(False, description="Status indicating request failure")
    detail: str = Field(..., description="Detailed description of the error")
    error_type: Optional[str] = Field(None, description="Category of error encountered")

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PredictionHistoryItem(BaseModel):
    """Summary item for scan history list view."""
    id: str = Field(..., description="Unique prediction identifier")
    filename: str = Field(..., description="Original image filename")
    crop: str = Field(..., description="Identified crop")
    disease: str = Field(..., description="Diagnosed condition")
    confidence: float = Field(..., description="Prediction confidence score (0-100)")
    severity: str = Field(..., description="Severity classification")
    is_healthy: bool = Field(False, description="Whether crop is healthy")
    created_at: datetime = Field(..., description="Timestamp of scan")


class PredictionHistoryDetail(PredictionHistoryItem):
    """Detailed view of a past scan record."""
    user_id: Optional[str] = Field(None, description="Owner ID if authenticated")
    image_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Image technical properties")


class PredictionHistoryListResponse(BaseModel):
    """Paginated list response of prediction history."""
    total: int = Field(..., description="Total records count")
    items: List[PredictionHistoryItem] = Field(..., description="List of past scans")

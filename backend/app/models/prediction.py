from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class PredictionDBModel(BaseModel):
    """
    MongoDB schema representation for the 'predictions' collection.
    
    Fields align with Phase 6 requirements:
    - _id / id
    - user_id (optional for guest scans; required once Phase 7 auth is attached)
    - image reference / metadata (avoids storing binary blobs directly in MongoDB)
    - crop, disease, confidence, severity
    - created_at
    """
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[str] = Field(None, alias="_id")
    user_id: Optional[str] = Field(None, description="Owner user ID if authenticated")
    filename: str = Field(..., description="Uploaded image filename")
    image_path: Optional[str] = Field(None, description="External storage reference or URI")
    crop: str = Field(..., description="Predicted crop species")
    disease: str = Field(..., description="Diagnosed condition or 'Healthy'")
    confidence: float = Field(..., description="Model confidence percentage (0-100)")
    severity: str = Field(..., description="Estimated disease severity")
    is_healthy: bool = Field(False, description="Whether leaf is diagnosed healthy")
    image_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Dimensions and format details")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of diagnosis")

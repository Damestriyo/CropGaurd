from typing import List, Optional
from pydantic import BaseModel, Field


class DiseaseBase(BaseModel):
    """Base schema for crop disease details."""
    id: str = Field(..., description="Unique slug identifier (e.g., tomato-early-blight)")
    crop: str = Field(..., description="Target crop name (e.g., Tomato)")
    disease: str = Field(..., description="Disease name or 'Healthy'")
    scientific_name: Optional[str] = Field(None, description="Botanical or pathogenic name")
    is_healthy: bool = Field(False, description="Flag indicating if leaf is healthy")
    severity: str = Field("Low", description="Typical severity level (Low, Moderate, High, Critical)")
    symptoms: List[str] = Field(default_factory=list, description="List of visual diagnostic symptoms")
    causes: List[str] = Field(default_factory=list, description="Fungal, bacterial, viral, or environmental causes")
    prevention: List[str] = Field(default_factory=list, description="Preventative cultural and agricultural practices")
    management: List[str] = Field(default_factory=list, description="Chemical and organic treatments for active infection")


class DiseaseDetailResponse(DiseaseBase):
    """Detailed response for a single disease query."""
    pass


class DiseaseListResponse(BaseModel):
    """Response containing a list of cataloged diseases."""
    total: int = Field(..., description="Total count of diseases returned")
    diseases: List[DiseaseBase] = Field(..., description="List of disease summaries")

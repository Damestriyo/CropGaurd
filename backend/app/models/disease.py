from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class DiseaseDBModel(BaseModel):
    """
    MongoDB schema representation for the 'diseases' collection (Phase 6/9).
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id", description="Unique disease slug")
    crop: str = Field(..., description="Crop name")
    disease: str = Field(..., description="Disease name")
    scientific_name: Optional[str] = Field(None, description="Botanical/pathogen name")
    severity: str = Field("Moderate", description="Default severity classification")
    is_healthy: bool = Field(False)
    symptoms: List[str] = Field(default_factory=list)
    causes: List[str] = Field(default_factory=list)
    prevention: List[str] = Field(default_factory=list)
    management: List[str] = Field(default_factory=list)

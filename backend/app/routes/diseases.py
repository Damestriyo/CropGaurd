from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.disease import DiseaseBase, DiseaseListResponse
from app.services.disease_service import DiseaseService
from app.schemas.prediction import APIErrorResponse

router = APIRouter(prefix="/diseases", tags=["Disease Knowledge Base"])


@router.get(
    "",
    response_model=DiseaseListResponse,
    status_code=status.HTTP_200_OK,
    summary="List cataloged crop diseases",
    description="Retrieve all documented crop diseases with symptoms and management recommendations. Optionally filter by crop name."
)
@router.get(
    "/",
    response_model=DiseaseListResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
def list_diseases(
    crop: Optional[str] = Query(None, description="Filter diseases by specific crop (e.g., Tomato, Potato, Corn)")
):
    """List diseases with optional crop filtering."""
    results = DiseaseService.get_all_diseases(crop=crop)
    return DiseaseListResponse(total=len(results), diseases=results)


@router.get(
    "/{disease_id}",
    response_model=DiseaseBase,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": APIErrorResponse, "description": "Disease record not found"}
    },
    summary="Get single disease details",
    description="Retrieve comprehensive diagnostic and agronomic treatment guidance for a specific disease by ID."
)
def get_disease(disease_id: str):
    """Retrieve disease by its unique slug ID."""
    record = DiseaseService.get_disease_by_id(disease_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disease record with ID '{disease_id}' was not found in the database."
        )
    return record

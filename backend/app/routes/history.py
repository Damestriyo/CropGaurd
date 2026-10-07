from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.history import PredictionHistoryListResponse, PredictionHistoryDetail
from app.services.history_service import HistoryService
from app.schemas.prediction import APIErrorResponse

router = APIRouter(prefix="/history", tags=["Prediction History"])


@router.get(
    "",
    response_model=PredictionHistoryListResponse,
    status_code=status.HTTP_200_OK,
    summary="List past prediction scans",
    description="Retrieve chronological history of previous crop disease scans."
)
@router.get(
    "/",
    response_model=PredictionHistoryListResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False
)
async def get_history(
    limit: int = Query(20, ge=1, le=100, description="Number of records to retrieve"),
    skip: int = Query(0, ge=0, description="Offset for pagination")
):
    """Retrieve history of previous predictions."""
    records = await HistoryService.get_history(limit=limit, skip=skip)
    return PredictionHistoryListResponse(total=len(records), items=records)


@router.get(
    "/{prediction_id}",
    response_model=PredictionHistoryDetail,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": APIErrorResponse, "description": "Prediction record not found"}
    },
    summary="Get single scan history detail",
    description="Retrieve technical and diagnostic details of a specific historical scan."
)
async def get_prediction_detail(prediction_id: str):
    """Retrieve details of a past prediction by ID."""
    record = await HistoryService.get_by_id(prediction_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction record '{prediction_id}' was not found."
        )
    return record


@router.delete(
    "/{prediction_id}",
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": APIErrorResponse, "description": "Prediction record not found"}
    },
    summary="Delete a past scan from history",
    description="Remove a prediction scan record by ID."
)
async def delete_prediction(prediction_id: str):
    """Delete a past prediction record."""
    deleted = await HistoryService.delete_by_id(prediction_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prediction record '{prediction_id}' not found or could not be deleted."
        )
    return {
        "success": True,
        "message": f"Prediction record '{prediction_id}' successfully deleted."
    }

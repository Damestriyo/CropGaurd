import logging
import uuid
from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId

from app.core.database import DatabaseManager
from app.models.prediction import PredictionDBModel
from app.schemas.prediction import ImageMetadata, PredictionResult

logger = logging.getLogger(__name__)

# In-memory buffer fallback when MongoDB service is not reachable
_IN_MEMORY_PREDICTIONS: List[PredictionDBModel] = []


class HistoryService:
    """Service handling persistence and retrieval of prediction scan history."""

    @classmethod
    async def record_prediction(
        cls,
        filename: str,
        image_metadata: ImageMetadata,
        prediction: PredictionResult,
        user_id: Optional[str] = None
    ) -> PredictionDBModel:
        """
        Saves a prediction record into MongoDB (or in-memory cache if DB is offline).
        Does NOT store binary image files directly in the database (adheres to specs).
        """
        record_id = str(ObjectId())
        now = datetime.now(timezone.utc)

        doc = {
            "_id": record_id,
            "user_id": user_id,
            "filename": filename,
            "image_path": None,
            "crop": prediction.crop,
            "disease": prediction.disease,
            "confidence": prediction.confidence,
            "severity": prediction.severity,
            "is_healthy": prediction.is_healthy,
            "image_metadata": image_metadata.model_dump() if hasattr(image_metadata, "model_dump") else image_metadata.dict(),
            "created_at": now
        }

        collection = DatabaseManager.get_collection("predictions")
        if collection is not None:
            try:
                await collection.insert_one(doc)
                logger.info("Saved prediction record %s to MongoDB.", record_id)
            except Exception as exc:
                logger.warning("Failed to insert prediction into MongoDB: %s. Using memory fallback.", exc)
                cls._store_in_memory(doc)
        else:
            cls._store_in_memory(doc)

        return PredictionDBModel(
            id=record_id,
            user_id=user_id,
            filename=filename,
            crop=prediction.crop,
            disease=prediction.disease,
            confidence=prediction.confidence,
            severity=prediction.severity,
            is_healthy=prediction.is_healthy,
            image_metadata=doc["image_metadata"],
            created_at=now
        )

    @classmethod
    def _store_in_memory(cls, doc: dict):
        """Stores prediction in local buffer for resilience."""
        model = PredictionDBModel(
            id=doc["_id"],
            user_id=doc.get("user_id"),
            filename=doc["filename"],
            crop=doc["crop"],
            disease=doc["disease"],
            confidence=doc["confidence"],
            severity=doc["severity"],
            is_healthy=doc.get("is_healthy", False),
            image_metadata=doc.get("image_metadata", {}),
            created_at=doc["created_at"]
        )
        _IN_MEMORY_PREDICTIONS.insert(0, model)
        # Cap memory buffer size
        if len(_IN_MEMORY_PREDICTIONS) > 100:
            _IN_MEMORY_PREDICTIONS.pop()

    @classmethod
    async def get_history(
        cls,
        user_id: Optional[str] = None,
        limit: int = 20,
        skip: int = 0
    ) -> List[PredictionDBModel]:
        """
        Retrieves prediction history, newest first.
        """
        collection = DatabaseManager.get_collection("predictions")
        if collection is not None:
            try:
                query = {}
                if user_id:
                    query["user_id"] = user_id

                cursor = collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
                records = []
                async for item in cursor:
                    records.append(
                        PredictionDBModel(
                            id=str(item["_id"]),
                            user_id=item.get("user_id"),
                            filename=item["filename"],
                            crop=item["crop"],
                            disease=item["disease"],
                            confidence=item["confidence"],
                            severity=item["severity"],
                            is_healthy=item.get("is_healthy", False),
                            image_metadata=item.get("image_metadata", {}),
                            created_at=item["created_at"]
                        )
                    )
                return records
            except Exception as exc:
                logger.warning("Error fetching from MongoDB: %s. Using memory fallback.", exc)

        # Fallback to in-memory store
        items = _IN_MEMORY_PREDICTIONS
        if user_id:
            items = [p for p in items if p.user_id == user_id]
        return items[skip : skip + limit]

    @classmethod
    async def get_by_id(cls, prediction_id: str, user_id: Optional[str] = None) -> Optional[PredictionDBModel]:
        """Retrieves a single prediction record by ID."""
        collection = DatabaseManager.get_collection("predictions")
        if collection is not None:
            try:
                query = {"_id": prediction_id}
                if user_id:
                    query["user_id"] = user_id
                doc = await collection.find_one(query)
                if doc:
                    return PredictionDBModel(
                        id=str(doc["_id"]),
                        user_id=doc.get("user_id"),
                        filename=doc["filename"],
                        crop=doc["crop"],
                        disease=doc["disease"],
                        confidence=doc["confidence"],
                        severity=doc["severity"],
                        is_healthy=doc.get("is_healthy", False),
                        image_metadata=doc.get("image_metadata", {}),
                        created_at=doc["created_at"]
                    )
            except Exception as exc:
                logger.warning("Error fetching prediction by ID from MongoDB: %s", exc)

        for p in _IN_MEMORY_PREDICTIONS:
            if p.id == prediction_id:
                if user_id and p.user_id != user_id:
                    return None
                return p
        return None

    @classmethod
    async def delete_by_id(cls, prediction_id: str, user_id: Optional[str] = None) -> bool:
        """Deletes a prediction record by ID."""
        collection = DatabaseManager.get_collection("predictions")
        if collection is not None:
            try:
                query = {"_id": prediction_id}
                if user_id:
                    query["user_id"] = user_id
                res = await collection.delete_one(query)
                return res.deleted_count > 0
            except Exception as exc:
                logger.warning("Error deleting prediction from MongoDB: %s", exc)

        for idx, p in enumerate(_IN_MEMORY_PREDICTIONS):
            if p.id == prediction_id:
                if user_id and p.user_id != user_id:
                    return False
                _IN_MEMORY_PREDICTIONS.pop(idx)
                return True
        return False

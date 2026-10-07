import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.core.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages the MongoDB asynchronous connection lifecycle."""

    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    is_connected: bool = False

    @classmethod
    async def connect(cls):
        """
        Connects to MongoDB and verifies the connection via a ping command.
        Gracefully handles connection errors so the API continues functioning
        even if a local MongoDB instance is not yet running.
        """
        try:
            logger.info("Connecting to MongoDB at: %s", settings.MONGODB_URL.split("@")[-1])
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=2500
            )
            cls.db = cls.client[settings.DATABASE_NAME]

            # Fast ping to verify host connectivity
            await cls.client.admin.command("ping")
            cls.is_connected = True
            logger.info("Successfully connected to MongoDB database: '%s'", settings.DATABASE_NAME)

            # Ensure optimal indexes
            await cls._ensure_indexes()

        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as exc:
            cls.is_connected = False
            cls.db = None
            logger.warning(
                "MongoDB connection could not be established: %s. "
                "The application will run in decoupled mode (in-memory/mock fallback).",
                exc
            )

    @classmethod
    async def disconnect(cls):
        """Closes the MongoDB connection gracefully."""
        if cls.client:
            cls.client.close()
            cls.is_connected = False
            cls.db = None
            logger.info("MongoDB connection closed.")

    @classmethod
    async def _ensure_indexes(cls):
        """Creates indexes for queries in predictions, users, and diseases collections."""
        if cls.db is not None:
            try:
                # Predictions index for quick user history queries and descending timestamps
                await cls.db.predictions.create_index([("created_at", -1)])
                await cls.db.predictions.create_index([("user_id", 1), ("created_at", -1)])

                # Users unique email index for Phase 7 authentication
                await cls.db.users.create_index([("email", 1)], unique=True)

                # Diseases index for rapid crop / slug filtering
                await cls.db.diseases.create_index([("id", 1)], unique=True)
                await cls.db.diseases.create_index([("crop", 1)])
            except Exception as index_err:
                logger.warning("Index creation warning: %s", index_err)

    @classmethod
    def get_collection(cls, collection_name: str):
        """Returns a collection handle if connected, else None."""
        if cls.is_connected and cls.db is not None:
            return cls.db[collection_name]
        return None


# Helper function to access the active database
def get_db() -> Optional[AsyncIOMotorDatabase]:
    """Dependency / helper for retrieving the active MongoDB database."""
    return DatabaseManager.db

import os
from typing import List, Set
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables with sensible defaults."""

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "AI Crop Disease Detection API")
    PROJECT_DESCRIPTION: str = "Backend API for deep learning-based crop disease classification"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

    # CORS configuration
    raw_origins = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173"
    )
    ALLOWED_ORIGINS: List[str] = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

    # Database Configuration (MongoDB)
    MONGODB_URL: str = os.getenv("MONGODB_URL") or os.getenv("MONGODB_URI") or "mongodb://localhost:27017"
    DATABASE_NAME: str = os.getenv("DATABASE_NAME") or os.getenv("MONGODB_DB_NAME") or "crop_disease_db"

    # Upload validation settings
    MAX_IMAGE_SIZE_MB: int = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
    MAX_IMAGE_SIZE_BYTES: int = MAX_IMAGE_SIZE_MB * 1024 * 1024

    raw_exts = os.getenv("ALLOWED_IMAGE_EXTENSIONS", ".jpg,.jpeg,.png,.webp")
    ALLOWED_IMAGE_EXTENSIONS: Set[str] = {ext.strip().lower() for ext in raw_exts.split(",") if ext.strip()}

    raw_mimes = os.getenv("ALLOWED_IMAGE_MIME_TYPES", "image/jpeg,image/png,image/webp")
    ALLOWED_IMAGE_MIME_TYPES: Set[str] = {mime.strip().lower() for mime in raw_mimes.split(",") if mime.strip()}


settings = Settings()

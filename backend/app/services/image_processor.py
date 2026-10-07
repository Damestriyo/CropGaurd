import io
import os
from typing import Tuple
from fastapi import UploadFile, HTTPException, status
from PIL import Image, UnidentifiedImageError

from app.core.config import settings
from app.schemas.prediction import ImageMetadata


class ImageProcessorService:
    """Service handling image upload validation, safe reading, and metadata extraction."""

    @staticmethod
    async def read_and_validate_file(file: UploadFile) -> bytes:
        """
        Validates file metadata, checks size limits, and returns the raw file bytes.

        Raises:
            HTTPException (400): If filename is missing or file is empty.
            HTTPException (415): If file extension or MIME type is not allowed.
            HTTPException (413): If file size exceeds the allowed threshold.
        """
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file must have a valid filename."
            )

        # 1. Validate file extension
        _, ext = os.path.splitext(file.filename)
        ext = ext.lower()
        if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
            allowed = ", ".join(sorted(settings.ALLOWED_IMAGE_EXTENSIONS))
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported file extension '{ext}'. Allowed extensions are: {allowed}"
            )

        # 2. Validate MIME type header provided by client
        if file.content_type and file.content_type.lower() not in settings.ALLOWED_IMAGE_MIME_TYPES:
            allowed = ", ".join(sorted(settings.ALLOWED_IMAGE_MIME_TYPES))
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Unsupported MIME type '{file.content_type}'. Allowed types are: {allowed}"
            )

        # 3. Read file content safely, guarding against memory bloat
        # Read up to MAX_IMAGE_SIZE_BYTES + 1024 bytes to detect oversized files early
        max_bytes = settings.MAX_IMAGE_SIZE_BYTES
        contents = await file.read(max_bytes + 1024)

        if len(contents) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty (0 bytes)."
            )

        if len(contents) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed limit of {settings.MAX_IMAGE_SIZE_MB} MB."
            )

        return contents

    @staticmethod
    def inspect_and_verify_image(contents: bytes, filename: str, content_type: str) -> Tuple[Image.Image, ImageMetadata]:
        """
        Safely verifies the integrity of the image using Pillow and extracts its metadata.

        Raises:
            HTTPException (400): If the byte stream is corrupted or cannot be parsed as an image.
        """
        try:
            # First pass: Pillow verify() to check image integrity without full decoding
            with Image.open(io.BytesIO(contents)) as test_img:
                test_img.verify()
        except (UnidentifiedImageError, Exception) as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or corrupted image file. Unable to decode image data."
            ) from exc

        # Second pass: Re-open for actual reading (verify() invalidates internal file pointers)
        image = Image.open(io.BytesIO(contents))
        img_format = image.format or "UNKNOWN"
        img_mode = image.mode
        width, height = image.size

        # Channel mapping based on mode
        channel_map = {
            "RGB": 3,
            "RGBA": 4,
            "L": 1,
            "CMYK": 4,
            "YCbCr": 3,
            "P": 3
        }
        channels = channel_map.get(img_mode, len(image.getbands()))
        size_bytes = len(contents)
        size_kb = round(size_bytes / 1024.0, 2)

        metadata = ImageMetadata(
            filename=filename,
            content_type=content_type or f"image/{img_format.lower()}",
            size_bytes=size_bytes,
            size_kb=size_kb,
            width=width,
            height=height,
            format=img_format,
            mode=img_mode,
            channels=channels
        )

        return image, metadata

    @staticmethod
    def prepare_rgb_image(image: Image.Image, target_size: Tuple[int, int] = None) -> Image.Image:
        """
        Converts the image to standard RGB mode and optionally resizes it.
        This provides the foundation for Phase 3 (model preprocessing).
        """
        if image.mode != "RGB":
            image = image.convert("RGB")

        if target_size:
            image = image.resize(target_size, resample=Image.Resampling.BILINEAR)

        return image

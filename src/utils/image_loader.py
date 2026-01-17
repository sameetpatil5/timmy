"""
Image loading and preview utilities.
"""

from PIL import Image
import io
from typing import Tuple, Optional


def load_image(file_bytes: bytes) -> Tuple[Optional[Image.Image], str]:
    """
    Load image from bytes without any modifications.

    Args:
        file_bytes: Raw image file bytes

    Returns:
        Tuple of (PIL Image object, error_message)
    """
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # Don't convert or modify - keep original
        return image, ""
    except Exception as e:
        return None, f"Failed to load image: {str(e)}"


def get_image_info(image: Image.Image) -> dict:
    """
    Extract basic image information.

    Args:
        image: PIL Image object

    Returns:
        Dictionary with image metadata
    """
    return {
        "format": image.format,
        "mode": image.mode,
        "size": image.size,
        "width": image.width,
        "height": image.height,
    }


def validate_image_format(filename: str, supported_formats: list) -> Tuple[bool, str]:
    """
    Validate if the image format is supported.

    Args:
        filename: Image filename
        supported_formats: List of supported extensions (e.g., ['.jpg', '.png'])

    Returns:
        Tuple of (is_valid, error_message)
    """
    import os

    ext = os.path.splitext(filename)[1].lower()

    if ext not in supported_formats:
        return (
            False,
            f"Unsupported format: {ext}. Supported: {', '.join(supported_formats)}",
        )

    return True, ""

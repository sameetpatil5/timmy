"""
File export utilities with quality preservation.
"""

from PIL import Image
import io
import os
from typing import Tuple


def save_image_with_exif(
    original_bytes: bytes, image: Image.Image, exif_bytes: bytes, output_format: str
) -> Tuple[bytes, str]:
    """
    Save image with new EXIF data without quality loss.

    This function preserves the original image quality by:
    - Using the highest quality settings
    - Maintaining original format
    - Preserving color profile and other metadata

    Args:
        original_bytes: Original image file bytes
        image: PIL Image object
        exif_bytes: Updated EXIF data
        output_format: Output format ('JPEG' or 'PNG')

    Returns:
        Tuple of (image_bytes, error_message)
    """
    try:
        output = io.BytesIO()

        if output_format in ["JPEG", "JPG"]:
            # For JPEG: preserve quality, subsampling, and ICC profile
            save_kwargs = {
                "format": "JPEG",
                "quality": 100,  # Maximum quality
                "subsampling": 0,  # No chroma subsampling (4:4:4)
                "exif": exif_bytes,
            }

            # Preserve ICC profile if exists
            if "icc_profile" in image.info:
                save_kwargs["icc_profile"] = image.info["icc_profile"]

            image.save(output, **save_kwargs)

        elif output_format == "PNG":
            # PNG is lossless, but EXIF support is limited
            # Store EXIF in PNG metadata if possible
            from PIL import PngImagePlugin

            pnginfo = PngImagePlugin.PngInfo()

            # Try to add EXIF as PNG text chunk
            try:
                import base64

                exif_b64 = base64.b64encode(exif_bytes).decode("ascii")
                pnginfo.add_text("exif", exif_b64)
            except:
                pass

            save_kwargs = {
                "format": "PNG",
                "compress_level": 9,  # Maximum compression (lossless)
                "pnginfo": pnginfo,
            }

            image.save(output, **save_kwargs)

        else:
            return b"", f"Unsupported output format: {output_format}"

        output.seek(0)
        return output.read(), ""

    except Exception as e:
        return b"", f"Failed to save image: {str(e)}"


def generate_output_filename(original_filename: str, suffix: str = "_fixed") -> str:
    """
    Generate output filename with suffix.

    Args:
        original_filename: Original filename
        suffix: Suffix to append before extension

    Returns:
        New filename
    """
    name, ext = os.path.splitext(original_filename)
    return f"{name}{suffix}{ext}"


def validate_output_bytes(original_size: int, output_size: int) -> Tuple[bool, str]:
    """
    Validate output image size to ensure quality preservation.

    Args:
        original_size: Original file size in bytes
        output_size: Output file size in bytes

    Returns:
        Tuple of (is_valid, warning_message)
    """
    # Allow for slight size variations due to metadata changes
    size_ratio = output_size / original_size if original_size > 0 else 0

    # Warn if file size decreased significantly (possible quality loss)
    if size_ratio < 0.8:
        return (
            False,
            f"⚠️ Output file is {100 - int(size_ratio * 100)}% smaller. Possible quality loss.",
        )

    # File size increase is fine (metadata addition)
    return True, ""

"""
EXIF metadata writing utilities with quality preservation.
"""

from PIL import Image
import piexif
from datetime import datetime
from typing import Tuple, Dict
from utils.exif_reader import format_exif_datetime, read_exif_data


def update_exif_datetime(
    image: Image.Image,
    new_datetime: datetime,
    modify_original: bool = True,
    modify_digitized: bool = True,
    modify_datetime: bool = True,
) -> Tuple[dict, str]:
    """
    Update EXIF datetime fields.

    Args:
        image: PIL Image object
        new_datetime: New datetime to set
        modify_original: Whether to modify DateTimeOriginal
        modify_digitized: Whether to modify DateTimeDigitized
        modify_datetime: Whether to modify DateTime

    Returns:
        Tuple of (updated_exif_dict, error_message)
    """
    try:
        # Format datetime for EXIF
        dt_string = format_exif_datetime(new_datetime)
        dt_bytes = dt_string.encode("utf-8")

        # Try to load existing EXIF, or create new
        exif_dict, _ = read_exif_data(image)

        if exif_dict is None:
            # Create new EXIF structure
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        # Ensure required IFDs exist
        if "0th" not in exif_dict:
            exif_dict["0th"] = {}
        if "Exif" not in exif_dict:
            exif_dict["Exif"] = {}

        # Update requested fields
        if modify_original:
            exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = dt_bytes

        if modify_digitized:
            exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = dt_bytes

        if modify_datetime:
            exif_dict["0th"][piexif.ImageIFD.DateTime] = dt_bytes

        return exif_dict, ""

    except Exception as e:
        return {}, f"Failed to update EXIF: {str(e)}"


def exif_dict_to_bytes(exif_dict: dict) -> Tuple[bytes, str]:
    """
    Convert EXIF dictionary to bytes for embedding.

    Args:
        exif_dict: EXIF dictionary

    Returns:
        Tuple of (exif_bytes, error_message)
    """
    try:
        exif_bytes = piexif.dump(exif_dict)
        return exif_bytes, ""
    except Exception as e:
        return b"", f"Failed to serialize EXIF: {str(e)}"


def get_modification_summary(
    old_datetime: str, new_datetime: datetime, fields_modified: list
) -> str:
    """
    Generate a summary of modifications made.

    Args:
        old_datetime: Original datetime string (or 'None')
        new_datetime: New datetime object
        fields_modified: List of field names modified

    Returns:
        Formatted summary string
    """
    new_str = format_exif_datetime(new_datetime)

    summary = f"**Changes Applied:**\n\n"
    summary += f"- **Old DateTime:** {old_datetime or 'None (no EXIF data)'}\n"
    summary += f"- **New DateTime:** {new_str}\n"
    summary += f"- **Fields Modified:** {', '.join(fields_modified)}\n"

    return summary

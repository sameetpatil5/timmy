"""
EXIF metadata reading utilities.
"""

from PIL import Image
import piexif
from typing import Optional, Dict, Tuple
from config.patterns import EXIF_DATETIME_FORMAT
from datetime import datetime


def read_exif_data(image: Image.Image) -> Tuple[Optional[dict], str]:
    """
    Read EXIF data from an image.

    Args:
        image: PIL Image object

    Returns:
        Tuple of (exif_dict, error_message)
    """
    try:
        exif_dict = piexif.load(image.info.get("exif", b""))
        return exif_dict, ""
    except Exception as e:
        # EXIF might not exist or be corrupted
        return None, f"No EXIF data or corrupted: {str(e)}"


def get_datetime_original(image: Image.Image) -> Optional[str]:
    """
    Extract DateTimeOriginal from EXIF if it exists.

    Args:
        image: PIL Image object

    Returns:
        DateTime string or None
    """
    try:
        exif_dict, error = read_exif_data(image)

        if exif_dict is None:
            return None

        # Try to get DateTimeOriginal from EXIF IFD
        if piexif.ExifIFD.DateTimeOriginal in exif_dict.get("Exif", {}):
            dt_bytes = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]
            return dt_bytes.decode("utf-8") if isinstance(dt_bytes, bytes) else dt_bytes

        # Fallback to DateTime from 0th IFD
        if piexif.ImageIFD.DateTime in exif_dict.get("0th", {}):
            dt_bytes = exif_dict["0th"][piexif.ImageIFD.DateTime]
            return dt_bytes.decode("utf-8") if isinstance(dt_bytes, bytes) else dt_bytes

        return None

    except Exception:
        return None


def format_exif_datetime(dt: datetime) -> str:
    """
    Format datetime object to EXIF datetime string format.

    Args:
        dt: datetime object

    Returns:
        Formatted string in EXIF format (YYYY:MM:DD HH:MM:SS)
    """
    return dt.strftime(EXIF_DATETIME_FORMAT)


def parse_exif_datetime(dt_string: str) -> Optional[datetime]:
    """
    Parse EXIF datetime string to datetime object.

    Args:
        dt_string: EXIF datetime string

    Returns:
        datetime object or None
    """
    try:
        return datetime.strptime(dt_string, EXIF_DATETIME_FORMAT)
    except Exception:
        return None


def get_all_datetime_fields(image: Image.Image) -> Dict[str, Optional[str]]:
    """
    Extract all datetime-related EXIF fields.

    Args:
        image: PIL Image object

    Returns:
        Dictionary with all datetime fields
    """
    result = {"DateTimeOriginal": None, "DateTimeDigitized": None, "DateTime": None}

    try:
        exif_dict, _ = read_exif_data(image)

        if exif_dict is None:
            return result

        # DateTimeOriginal
        if piexif.ExifIFD.DateTimeOriginal in exif_dict.get("Exif", {}):
            dt = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]
            result["DateTimeOriginal"] = (
                dt.decode("utf-8") if isinstance(dt, bytes) else dt
            )

        # DateTimeDigitized
        if piexif.ExifIFD.DateTimeDigitized in exif_dict.get("Exif", {}):
            dt = exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized]
            result["DateTimeDigitized"] = (
                dt.decode("utf-8") if isinstance(dt, bytes) else dt
            )

        # DateTime
        if piexif.ImageIFD.DateTime in exif_dict.get("0th", {}):
            dt = exif_dict["0th"][piexif.ImageIFD.DateTime]
            result["DateTime"] = dt.decode("utf-8") if isinstance(dt, bytes) else dt

    except Exception:
        pass

    return result


def has_valid_exif_datetime(image: Image.Image) -> Tuple[bool, Optional[datetime]]:
    """
    Check if the image has valid EXIF datetime information.

    Args:
        image: PIL Image object

    Returns:
        Tuple of (has_valid_datetime, datetime_object)
        Returns (True, datetime) if valid EXIF exists, (False, None) otherwise
    """
    try:
        # Get DateTimeOriginal first (most reliable)
        dt_string = get_datetime_original(image)

        if dt_string:
            # Try to parse it
            dt_obj = parse_exif_datetime(dt_string)
            if dt_obj:
                return True, dt_obj

        # Fallback: check all fields
        all_fields = get_all_datetime_fields(image)

        # Try each field in priority order
        for field in ["DateTimeOriginal", "DateTimeDigitized", "DateTime"]:
            if all_fields.get(field):
                dt_obj = parse_exif_datetime(all_fields[field])
                if dt_obj:
                    return True, dt_obj

        return False, None

    except Exception:
        return False, None

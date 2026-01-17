"""
Filename date pattern configurations for automatic parsing.
"""

import re
from typing import List, Dict

# Date patterns with regex and format string
FILENAME_PATTERNS: List[Dict[str, str]] = [
    {
        "name": "WhatsApp IMG Format",
        "pattern": r"IMG[-_](\d{4})(\d{2})(\d{2})",
        "example": "IMG-20241222-WA0135.jpg",
        "format": "%Y%m%d",
    },
    {
        "name": "ISO Date with Hyphens",
        "pattern": r"(\d{4})-(\d{2})-(\d{2})",
        "example": "2024-12-22-photo.jpg",
        "format": "%Y-%m-%d",
    },
    {
        "name": "ISO Date with Underscores",
        "pattern": r"(\d{4})_(\d{2})_(\d{2})",
        "example": "2024_12_22_photo.jpg",
        "format": "%Y_%m_%d",
    },
    {
        "name": "Compact Date YYYYMMDD",
        "pattern": r"(\d{4})(\d{2})(\d{2})",
        "example": "20241222_photo.jpg",
        "format": "%Y%m%d",
    },
    {
        "name": "Date DDMMYYYY",
        "pattern": r"(\d{2})(\d{2})(\d{4})",
        "example": "22122024_photo.jpg",
        "format": "%d%m%Y",
        "ambiguous": True,
    },
]

# EXIF datetime format
EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"

# Supported image formats
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png"]

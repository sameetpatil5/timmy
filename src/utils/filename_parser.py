"""
Filename parsing utilities for automatic and custom date extraction.
"""

import re
from datetime import datetime
from typing import Optional, Tuple, Dict
from config.patterns import FILENAME_PATTERNS
from utils.validators import validate_date, is_ambiguous_date


def parse_filename_auto(filename: str) -> Tuple[Optional[datetime], str, bool]:
    """
    Automatically parse date from filename using predefined patterns.

    Args:
        filename: The image filename

    Returns:
        Tuple of (datetime_object, confidence_message, is_ambiguous)
    """
    for pattern_info in FILENAME_PATTERNS:
        pattern = pattern_info["pattern"]
        match = re.search(pattern, filename)

        if match:
            groups = match.groups()

            # Determine year, month, day based on pattern type
            if pattern_info.get("format") == "%d%m%Y":
                # DDMMYYYY format
                day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
            else:
                # YYYYMMDD or similar formats
                year, month, day = int(groups[0]), int(groups[1]), int(groups[2])

            # Validate the date
            is_valid, error_msg = validate_date(year, month, day)

            if not is_valid:
                continue

            # Create datetime object
            dt = datetime(year, month, day, 12, 0, 0)  # Default to noon

            # Check for ambiguity
            ambiguous = pattern_info.get("ambiguous", False) and is_ambiguous_date(
                day, month
            )

            confidence = f"✔ Detected using pattern: {pattern_info['name']}"
            if ambiguous:
                confidence = f"⚠ Ambiguous date detected (could be DD/MM or MM/DD): {pattern_info['name']}"

            return dt, confidence, ambiguous

    return None, "❌ No date pattern detected in filename", False


def parse_filename_custom(
    filename: str, custom_pattern: str
) -> Tuple[Optional[datetime], str]:
    """
    Parse date from filename using a custom user-defined pattern.

    Args:
        filename: The image filename
        custom_pattern: User-defined pattern (e.g., "IMG-{YYYY}{MM}{DD}-WA")

    Returns:
        Tuple of (datetime_object, message)
    """
    try:
        # Convert custom pattern to regex
        regex_pattern = custom_pattern
        regex_pattern = regex_pattern.replace("{YYYY}", r"(\d{4})")
        regex_pattern = regex_pattern.replace("{MM}", r"(\d{2})")
        regex_pattern = regex_pattern.replace("{DD}", r"(\d{2})")
        regex_pattern = regex_pattern.replace("{HH}", r"(\d{2})")
        regex_pattern = regex_pattern.replace("{mm}", r"(\d{2})")
        regex_pattern = regex_pattern.replace("{SS}", r"(\d{2})")

        # Escape special characters except our groups
        # This is a simplified approach - more robust escaping may be needed

        match = re.search(regex_pattern, filename)

        if not match:
            return None, f"❌ Filename doesn't match pattern: {custom_pattern}"

        groups = match.groups()

        # Extract components based on pattern order
        pattern_parts = re.findall(r"\{(YYYY|MM|DD|HH|mm|SS)\}", custom_pattern)

        components = {}
        for i, part in enumerate(pattern_parts):
            if i < len(groups):
                components[part] = int(groups[i])

        # Build datetime
        year = components.get("YYYY", datetime.now().year)
        month = components.get("MM", 1)
        day = components.get("DD", 1)
        hour = components.get("HH", 12)
        minute = components.get("mm", 0)
        second = components.get("SS", 0)

        # Validate
        is_valid, error_msg = validate_date(year, month, day)
        if not is_valid:
            return None, f"❌ {error_msg}"

        dt = datetime(year, month, day, hour, minute, second)
        return dt, f"✔ Successfully parsed: {dt.strftime('%Y-%m-%d %H:%M:%S')}"

    except Exception as e:
        return None, f"❌ Error parsing with custom pattern: {str(e)}"


def get_pattern_examples() -> str:
    """
    Get example patterns for user reference.

    Returns:
        Formatted string with pattern examples
    """
    examples = []
    for pattern in FILENAME_PATTERNS:
        examples.append(f"- {pattern['example']} → {pattern['name']}")

    return "\n".join(examples)

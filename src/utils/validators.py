"""
Validation utilities for dates, formats, and user inputs.
"""

from datetime import datetime
from typing import Tuple, Optional
import re


def validate_date(year: int, month: int, day: int) -> Tuple[bool, str]:
    """
    Validate if the given date components form a valid date.

    Args:
        year: Year component
        month: Month component
        day: Day component

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        date_obj = datetime(year, month, day)

        # Check if date is in the future
        if date_obj > datetime.now():
            return False, f"Date {year}-{month:02d}-{day:02d} is in the future"

        # Check if date is too old (before 1970)
        if year < 1970:
            return False, f"Year {year} seems too old for a digital photo"

        return True, ""
    except ValueError as e:
        return False, f"Invalid date: {str(e)}"


def validate_datetime(
    dt_string: str, format_string: str
) -> Tuple[bool, str, Optional[datetime]]:
    """
    Validate a datetime string against a format.

    Args:
        dt_string: The datetime string to validate
        format_string: The expected format

    Returns:
        Tuple of (is_valid, error_message, datetime_object)
    """
    try:
        dt_obj = datetime.strptime(dt_string, format_string)

        if dt_obj > datetime.now():
            return False, "Date is in the future", None

        if dt_obj.year < 1970:
            return False, "Year seems too old for a digital photo", None

        return True, "", dt_obj
    except ValueError as e:
        return False, f"Invalid datetime format: {str(e)}", None


def validate_custom_pattern(pattern: str) -> Tuple[bool, str]:
    """
    Validate a custom filename pattern provided by the user.

    Args:
        pattern: User-provided pattern string

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not pattern:
        return False, "Pattern cannot be empty"

    # Check for required date components
    required = ["{YYYY}", "{MM}", "{DD}"]
    has_all = all(comp in pattern for comp in required)

    if not has_all:
        return False, "Pattern must contain {YYYY}, {MM}, and {DD}"

    return True, ""


def is_ambiguous_date(day: int, month: int) -> bool:
    """
    Check if a date could be ambiguous (day and month could be swapped).

    Args:
        day: Day component
        month: Month component

    Returns:
        True if ambiguous (both <= 12), False otherwise
    """
    return day <= 12 and month <= 12

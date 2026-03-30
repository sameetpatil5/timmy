"""
Batch processing utilities for handling multiple images.
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
from PIL import Image
import io
import os

from utils.image_loader import load_image
from utils.exif_reader import has_valid_exif_datetime, get_datetime_original
from utils.filename_parser import parse_filename_auto
from utils.exif_writer import update_exif_datetime, exif_dict_to_bytes
from utils.file_exporter import save_image_with_exif, generate_output_filename, insert_exif_lossless


class ImageBatchItem:
    """Represents a single image in a batch processing queue."""

    def __init__(self, filename: str, file_bytes: bytes, index: int):
        self.filename = filename
        self.file_bytes = file_bytes
        self.index = index
        self.image = None
        self.load_error = None

        # EXIF status
        self.has_exif = False
        self.exif_datetime = None

        # Filename parsing
        self.filename_datetime = None
        self.filename_parse_message = ""

        # User decisions
        self.action = "keep"  # Options: "keep", "filename", "manual"
        self.manual_datetime = None

        # Processing results
        self.processed = False
        self.output_bytes = None
        self.output_filename = None
        self.error_message = None

    def load(self) -> bool:
        """Load and analyze the image."""
        self.image, self.load_error = load_image(self.file_bytes)

        if self.image is None:
            return False

        # Check for existing EXIF
        self.has_exif, self.exif_datetime = has_valid_exif_datetime(self.image)

        # Try to parse filename
        parsed_dt, message, _ = parse_filename_auto(self.filename)
        self.filename_datetime = parsed_dt
        self.filename_parse_message = message

        return True

    def get_target_datetime(self) -> Optional[datetime]:
        """Get the target datetime based on current action setting."""
        if self.action == "keep":
            return self.exif_datetime if self.has_exif else self.filename_datetime
        elif self.action == "filename":
            return self.filename_datetime
        elif self.action == "manual":
            return self.manual_datetime
        return None

    def get_status_summary(self) -> Dict[str, str]:
        """Get a summary of the current status."""
        return {
            "filename": self.filename,
            "has_exif": "✅ Yes" if self.has_exif else "❌ No",
            "exif_date": (
                self.exif_datetime.strftime("%Y-%m-%d %H:%M:%S")
                if self.exif_datetime
                else "N/A"
            ),
            "filename_date": (
                self.filename_datetime.strftime("%Y-%m-%d %H:%M:%S")
                if self.filename_datetime
                else "N/A"
            ),
            "action": self.action,
            "target_date": (
                self.get_target_datetime().strftime("%Y-%m-%d %H:%M:%S")
                if self.get_target_datetime()
                else "N/A"
            ),
        }


class BatchProcessor:
    """Handles batch processing of multiple images."""

    def __init__(self):
        self.items: List[ImageBatchItem] = []
        self.total_count = 0
        self.loaded_count = 0
        self.processed_count = 0

    def add_files(self, uploaded_files) -> int:
        """
        Add uploaded files to the batch.

        Args:
            uploaded_files: Streamlit uploaded files

        Returns:
            Number of files added
        """
        count = 0
        for i, uploaded_file in enumerate(uploaded_files):
            file_bytes = uploaded_file.read()
            filename = uploaded_file.name

            item = ImageBatchItem(filename, file_bytes, i)
            self.items.append(item)
            count += 1

        self.total_count = len(self.items)
        return count

    def load_all(self) -> Tuple[int, int]:
        """
        Load and analyze all images in the batch.

        Returns:
            Tuple of (successful_count, failed_count)
        """
        success = 0
        failed = 0

        for item in self.items:
            if item.load():
                success += 1
            else:
                failed += 1

        self.loaded_count = success
        return success, failed

    def set_all_actions(self, action: str, manual_datetime: Optional[datetime] = None):
        """
        Set the same action for all items.

        Args:
            action: Action to apply ("keep", "filename", "manual")
            manual_datetime: If action is "manual", the datetime to use
        """
        for item in self.items:
            item.action = action
            if action == "manual" and manual_datetime:
                item.manual_datetime = manual_datetime

    def process_all(
        self,
        modify_original: bool = True,
        modify_digitized: bool = True,
        modify_datetime: bool = True,
        suffix: str = "_fixed",
    ) -> Tuple[int, int]:
        """
        Process all items in the batch.

        Args:
            modify_original: Update DateTimeOriginal
            modify_digitized: Update DateTimeDigitized
            modify_datetime: Update DateTime
            suffix: Output filename suffix

        Returns:
            Tuple of (successful_count, failed_count)
        """
        success = 0
        failed = 0

        for item in self.items:
            if item.image is None:
                item.error_message = "Image not loaded"
                failed += 1
                continue

            target_dt = item.get_target_datetime()

            if target_dt is None:
                item.error_message = "No valid datetime available"
                failed += 1
                continue

            try:
                # Update EXIF
                exif_dict, exif_error = update_exif_datetime(
                    item.image,
                    target_dt,
                    modify_original,
                    modify_digitized,
                    modify_datetime,
                )

                if exif_error:
                    item.error_message = exif_error
                    failed += 1
                    continue

                # Convert to bytes
                exif_bytes, bytes_error = exif_dict_to_bytes(exif_dict)

                if bytes_error:
                    item.error_message = bytes_error
                    failed += 1
                    continue

                # Save image
                output_format = item.image.format if item.image.format else "JPEG"

                # output_bytes, save_error = save_image_with_exif(
                #     item.file_bytes, item.image, exif_bytes, output_format
                # )

                output_bytes, save_error = insert_exif_lossless(
                    item.file_bytes, exif_bytes
                )

                if save_error:
                    item.error_message = save_error
                    failed += 1
                    continue

                # Success
                item.output_bytes = output_bytes
                item.output_filename = generate_output_filename(item.filename, suffix)
                item.processed = True
                success += 1

            except Exception as e:
                item.error_message = f"Processing error: {str(e)}"
                failed += 1

        self.processed_count = success
        return success, failed

    def get_summary_table(self) -> List[Dict[str, str]]:
        """Get a summary table of all items."""
        return [item.get_status_summary() for item in self.items]

    def get_processed_items(self) -> List[ImageBatchItem]:
        """Get all successfully processed items."""
        return [item for item in self.items if item.processed]

    def get_failed_items(self) -> List[ImageBatchItem]:
        """Get all failed items."""
        return [
            item for item in self.items if not item.processed and item.image is not None
        ]

    def clear(self):
        """Clear all items from the batch."""
        self.items.clear()
        self.total_count = 0
        self.loaded_count = 0
        self.processed_count = 0

import streamlit as st
from PIL import Image
from datetime import datetime
from typing import Tuple

from utils.image_loader import get_image_info
from utils.exif_reader import get_all_datetime_fields, has_valid_exif_datetime


def render_exif_info_section(image, filename):

    # Image Information
    st.subheader("📋 Image Information")

    info = get_image_info(image)
    st.markdown(
        f"""
    **Filename:** `{filename}` &nbsp; | &nbsp;
    **Format:** {info['format']} &nbsp; | &nbsp;
    **Size:** {info['width']} × {info['height']} pixels &nbsp; | &nbsp;
    **Mode:** {info['mode']}
    """
    )

    # Get datetime fields
    datetime_fields = get_all_datetime_fields(image)

    # Display current EXIF dates
    st.write("**Current EXIF Dates:**")

    for field, value in datetime_fields.items():
        if value:
            st.write(f"- {field}: `{value}`")
        else:
            st.write(f"- {field}: *Not set*")

    # Check if valid EXIF datetime exists
    has_exif, exif_dt = has_valid_exif_datetime(image)

    # Show alert if EXIF already has valid date
    if has_exif:
        st.success(
            f"✅ **Valid EXIF date found:** {exif_dt.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        st.info(
            "💡 The output file will use this existing EXIF date. To override, use Manual Entry mode."
        )
    else:
        st.warning(
            "⚠️ **No valid EXIF date found.** Will extract from filename or use manual entry."
        )

    return has_exif, exif_dt

import streamlit as st

from .apply_changes_section import render_apply_changes_section
from .download_section import render_download_section

def render_apply_changes_and_download_section(
    image,
    file_bytes,
    use_existing_exif,
    target_datetime,
    modify_original,
    modify_digitized,
    modify_datetime,
    output_filename_preview,
    output_bytes,
):
    if not output_bytes:
        return

    apply_changes_section, download_section = st.columns(2)

    with apply_changes_section:
        render_apply_changes_section(
            image,
            file_bytes,
            use_existing_exif,
            target_datetime,
            modify_original,
            modify_digitized,
            modify_datetime,
            output_filename_preview,
            output_bytes,
        )

    with download_section:
        render_download_section(image)

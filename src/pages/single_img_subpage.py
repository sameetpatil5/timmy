import streamlit as st

from .components.single_subpage.image_preview_section import (
    render_preview_image_section,
)


from .components.single_subpage.exif_info_section import render_exif_info_section
from .components.single_subpage.extraction_modes_exif_updates_output_settings_section import (
    extraction_modes_exif_updates_output_settings_section,
)
from .components.single_subpage.apply_changes_download_section import (
    render_apply_changes_and_download_section,
)

def render_single_image_page(uploaded_file):
    # Read file bytes
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name

    # image = load_preview_image(file_bytes, filename)

    # has_exif, exif_dt, exif_preview = show_exif_info(image, filename)

    image_preview_col, exif_preview_col = st.columns([1, 2])

    # Load and Preview image
    with image_preview_col:
        image = render_preview_image_section(file_bytes, filename)

    # Load and Display EXIF Data and
    with exif_preview_col:
        has_exif, exif_dt = render_exif_info_section(image, filename)

    # ..
    (
        target_datetime,
        use_existing_exif,
        modify_original,
        modify_digitized,
        modify_datetime,
    ) = extraction_modes_exif_updates_output_settings_section(
        filename, image, has_exif, exif_dt
    )

    # ..

    render_apply_changes_and_download_section(
        image,
        file_bytes,
        use_existing_exif,
        target_datetime,
        modify_original,
        modify_digitized,
        modify_datetime,
        filename,
        file_bytes,
        )
    
    output_data = file_bytes

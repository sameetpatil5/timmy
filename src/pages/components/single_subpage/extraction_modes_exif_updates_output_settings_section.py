import streamlit as st

from .extraction_modes_section import render_extraction_modes_section
from .exif_update_section import render_exif_update_section
from .output_settings_section import render_output_settings_section

def extraction_modes_exif_updates_output_settings_section(filename, image, has_exif, exif_dt):
    extraction_modes, update_settings = st.columns(2)

    with extraction_modes:
        target_datetime, use_existing_exif = render_extraction_modes_section(
            filename, image, has_exif, exif_dt
        )

    with update_settings:
        modify_original, modify_digitized, modify_datetime = render_exif_update_section()
        render_output_settings_section(filename)

    return (
        target_datetime,
        use_existing_exif,
        modify_original,
        modify_digitized,
        modify_datetime,
    )

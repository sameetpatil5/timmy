import streamlit as st

from utils.batch_processor import BatchProcessor

from .components.multi_subpage.review_images_section import (
    render_review_images_section,
)
from .components.multi_subpage.batch_action_section import (
    render_batch_action_section,
)
from .components.multi_subpage.process_images_section import (
    render_process_images_section,
)
from .components.multi_subpage.download_section import render_download_section
from .components.multi_subpage.output_settings_section import (
    render_output_settings_section,
)
from .components.multi_subpage.exif_update_section import (
    render_exif_update_section,
)
from .components.multi_subpage.customize_individual_section import (
    render_customize_individual_section,
)


def render_multi_image_page(uploaded_files):

    # Initialize batch processor if needed
    if st.session_state.batch_processor is None or st.button("🔄 Reload Files"):
        st.session_state.batch_processor = BatchProcessor()

        with st.spinner(f"Loading {len(uploaded_files)} images..."):
            count = st.session_state.batch_processor.add_files(uploaded_files)
            success, failed = st.session_state.batch_processor.load_all()

        st.success(f"✅ Loaded {success} images successfully")
        if failed > 0:
            st.warning(f"⚠️ Failed to load {failed} images")

    batch = st.session_state.batch_processor

    review, options = st.columns([2, 1])

    with review:

        render_review_images_section(batch)

    with options:

        # Step 3: Choose batch action
        show_customize = render_batch_action_section(batch)

    if show_customize:
        render_customize_individual_section(batch)

    exif_update, output_settings = st.columns(2)

    with exif_update:
        # Step 4: EXIF field selection
        modify_original, modify_digitized, modify_datetime = (
            render_exif_update_section()
        )

    with output_settings:
        # Step 5: Output settings
        filename_suffix = render_output_settings_section()

    process, download = st.columns(2)

    with process:
        # Step 6: Process all
        render_process_images_section(
            batch, modify_original, modify_digitized, modify_datetime, filename_suffix
        )

    with download:
        # Step 7: Download results
        render_download_section(batch)

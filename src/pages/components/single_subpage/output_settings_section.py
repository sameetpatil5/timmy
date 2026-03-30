import streamlit as st

from utils.file_exporter import generate_output_filename


def render_output_settings_section(filename):

    # Output settings
    st.subheader("4️⃣ Output Settings")

    image_preview, image_info = st.columns([1, 2])

    with image_preview:
        filename_suffix = st.text_input(
            "Filename Suffix",
            value="_fixed",
            help="Suffix to append to the output filename",
        )

    with image_info:
        output_filename_preview = generate_output_filename(filename, filename_suffix)
        st.write(f"**Output filename:** `{output_filename_preview}`")

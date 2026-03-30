import streamlit as st
from utils.image_loader import load_image, validate_image_format
from config.patterns import SUPPORTED_FORMATS


def render_preview_image_section(file_bytes, filename):
    is_valid, error = validate_image_format(filename, SUPPORTED_FORMATS)

    if not is_valid:
        st.error(error)
        st.stop()

    image, err = load_image(file_bytes)

    if not image:
        st.error(err)
        st.stop()

    st.image(image)

    return image

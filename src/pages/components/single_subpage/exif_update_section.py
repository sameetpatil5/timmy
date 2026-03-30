import streamlit as st


def render_exif_update_section():
    # Metadata selection
    st.subheader("3️⃣ Select EXIF Fields to Update")

    image_preview, image_info, col3 = st.columns(3)

    with image_preview:
        modify_original = st.checkbox(
            "DateTimeOriginal", value=True, help="Primary capture date field"
        )

    with image_info:
        modify_digitized = st.checkbox(
            "DateTimeDigitized", value=True, help="Digitization date field"
        )

    with col3:
        modify_datetime = st.checkbox(
            "DateTime", value=True, help="File modification date"
        )

    if not any([modify_original, modify_digitized, modify_datetime]):
        st.warning("⚠️ Please select at least one field to modify.")

    return modify_original, modify_digitized, modify_datetime
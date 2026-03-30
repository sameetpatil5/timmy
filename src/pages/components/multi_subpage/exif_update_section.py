import streamlit as st

def render_exif_update_section():
    # Step 5: EXIF field selection
    st.subheader("4️⃣ Select EXIF Fields to Update")

    col1, col2, col3 = st.columns(3)

    with col1:
        modify_original = st.checkbox(
            "DateTimeOriginal", value=True, key="bulk_original"
        )

    with col2:
        modify_digitized = st.checkbox(
            "DateTimeDigitized", value=True, key="bulk_digitized"
        )

    with col3:
        modify_datetime = st.checkbox("DateTime", value=True, key="bulk_datetime")

    return modify_original, modify_digitized, modify_datetime

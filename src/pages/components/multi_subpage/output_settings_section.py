import streamlit as st

def render_output_settings_section():
    # Step 6: Output settings
    st.subheader("5️⃣ Output Settings")

    filename_suffix = st.text_input(
        "Filename Suffix", value="_fixed", key="bulk_suffix"
    )

    return filename_suffix

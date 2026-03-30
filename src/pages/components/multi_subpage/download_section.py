import streamlit as st
from datetime import datetime
import io
import zipfile


def zip_processed_images(batch):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for item in batch.get_processed_items():
            zip_file.writestr(item.output_filename, item.output_bytes)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def render_download_section(batch):
    # Step 8: Download results
    # if batch.processed_count > 0:
    st.subheader("7️⃣ Download Results")

    # # Create ZIP file
    # zip_buffer = io.BytesIO()
    # with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
    #     for item in batch.get_processed_items():
    #         zip_file.writestr(item.output_filename, item.output_bytes)

    # zip_buffer.seek(0)

    col1, col2 = st.columns([3, 1])

    with col1:
        zip_data = zip_processed_images(batch) if batch.processed_count > 0 else b""

        st.download_button(
            label=f"⬇️ Download All ({batch.processed_count} images) as ZIP",
            data=zip_data,
            file_name=f"fixed_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip",
            type="primary",
            width="stretch",
            disabled=batch.processed_count == 0,
        )

    with col2:
        if st.button("🗑️ Clear All", width="stretch"):
            st.session_state.batch_processor = None
            st.rerun()

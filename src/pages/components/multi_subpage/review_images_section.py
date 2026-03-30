import streamlit as st
import pandas as pd

def render_review_images_section(batch):

    if batch.loaded_count > 0:

        # Step 2: Review loaded images
        st.subheader("2️⃣ Review Detected Dates")

        # Create summary table
        summary_data = []
        for item in batch.items:
            if item.image is not None:
                summary_data.append(
                    {
                        "Filename": item.filename,
                        "Has EXIF": "✅" if item.has_exif else "❌",
                        "EXIF Date": (
                            item.exif_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            if item.exif_datetime
                            else "N/A"
                        ),
                        "Filename Date": (
                            item.filename_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            if item.filename_datetime
                            else "Not detected"
                        ),
                    }
                )

        df = pd.DataFrame(summary_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Images", batch.loaded_count)
        with col2:
            has_exif_count = sum(1 for item in batch.items if item.has_exif)
            st.metric("Has EXIF", has_exif_count)
        with col3:
            no_exif_count = batch.loaded_count - has_exif_count
            st.metric("No EXIF", no_exif_count)
        with col4:
            filename_detected = sum(
                1 for item in batch.items if item.filename_datetime is not None
            )
            st.metric("Filename Detected", filename_detected)

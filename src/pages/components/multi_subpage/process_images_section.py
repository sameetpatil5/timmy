import streamlit as st
import pandas as pd


def render_process_images_section(
    batch, modify_original, modify_digitized, modify_datetime, filename_suffix
):
    # Step 7: Process all
    st.subheader("6️⃣ Process All Images")

    if st.button("🚀 Process All Images", type="primary", use_container_width=True):

        with st.spinner(f"Processing {batch.loaded_count} images..."):
            success, failed = batch.process_all(
                modify_original,
                modify_digitized,
                modify_datetime,
                filename_suffix,
            )

        st.success(f"✅ Successfully processed {success} images!")
        if failed > 0:
            st.error(f"❌ Failed to process {failed} images")

            # Show failed items
            with st.expander("View Failed Images"):
                for item in batch.get_failed_items():
                    st.write(f"- {item.filename}: {item.error_message}")

        # Summary table
        st.write("**Processed Images:**")
        result_data = []
        for item in batch.get_processed_items():
            target = item.get_target_datetime()
            result_data.append(
                {
                    "Filename": item.filename,
                    "Output": item.output_filename,
                    "Final Date": (
                        target.strftime("%Y-%m-%d %H:%M:%S") if target else "N/A"
                    ),
                    "Size": f"{len(item.output_bytes):,} bytes",
                }
            )

        df_results = pd.DataFrame(result_data)
        st.dataframe(df_results, use_container_width=True, hide_index=True)

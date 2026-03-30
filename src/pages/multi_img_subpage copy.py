import streamlit as st

import pandas as pd
from datetime import datetime, time

import io
import zipfile

from utils.batch_processor import BatchProcessor

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

    with options:

        # Step 3: Choose batch action
        st.subheader("3️⃣ Choose Batch Action")

        batch_action = st.radio(
            "Select action for all images:",
            [
                "Keep Existing/Extracted (Smart Default)",
                "Use Filename Date for All",
                "Set Manual Date for All",
                "Customize Individual Images",
            ],
            key="radio_batch_action",
            help="Choose how to handle all images at once",
        )

        manual_batch_datetime = None

        if batch_action == "Keep Existing/Extracted (Smart Default)":
            st.info(
                "ℹ️ **Smart Default:** Uses existing EXIF if available, otherwise extracts from filename."
            )
            batch.set_all_actions("keep")

        elif batch_action == "Use Filename Date for All":
            st.info(
                "ℹ️ **Filename Mode:** Extracts date from filename for all images (ignores existing EXIF)."
            )
            batch.set_all_actions("filename")

        elif batch_action == "Set Manual Date for All":
            st.warning(
                "⚠️ **Manual Mode:** Sets the SAME date and time for ALL images."
            )

            col1, col2 = st.columns(2)
            with col1:
                manual_date = st.date_input(
                    "Date for all images", value=datetime.now().date()
                )
            with col2:
                manual_time = st.time_input(
                    "Time for all images", value=time(12, 0, 0)
                )

            manual_batch_datetime = datetime.combine(manual_date, manual_time)
            batch.set_all_actions("manual", manual_batch_datetime)

            st.success(
                f"✅ Will set all images to: {manual_batch_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    # Step 4: Customize individual images (optional)
    if batch_action == "Customize Individual Images":
        st.subheader("Customize Individual Images")

        with st.expander("🔧 Advanced: Customize Each Image", expanded=False):
            st.info(
                "💡 Change the action for specific images below. Leave unchanged to use the batch action."
            )

            for i, item in enumerate(batch.items):
                if item.image is None:
                    continue

                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 2, 1, 2])

                    with col1:
                        st.write(f"**{item.filename}**")

                    with col2:
                        st.image(item.image, width=200)

                    with col3:
                        current_action = st.selectbox(
                            f"Action",
                            ["keep", "filename", "manual"],
                            index=["keep", "filename", "manual"].index(
                                item.action
                            ),
                            key=f"action_{i}",
                            label_visibility="collapsed",
                        )
                        item.action = current_action

                    with col4:
                        if current_action == "manual":
                            manual_dt = st.text_input(
                                "Date (YYYY-MM-DD HH:MM:SS)",
                                value=(
                                    item.manual_datetime.strftime("%Y-%m-%d %H:%M:%S")
                                    if item.manual_datetime
                                    else ""
                                ),
                                key=f"manual_{i}",
                                label_visibility="collapsed",
                                placeholder="YYYY-MM-DD HH:MM:SS",
                            )
                            try:
                                item.manual_datetime = datetime.strptime(
                                    manual_dt, "%Y-%m-%d %H:%M:%S"
                                )
                            except:
                                st.error("Invalid format")
                        else:
                            target = item.get_target_datetime()
                            if target:
                                st.write(
                                    f"→ {target.strftime('%Y-%m-%d %H:%M:%S')}"
                                )
                            else:
                                st.write("→ N/A")

                    st.divider()

    exif_update, output_settings = st.columns(2)

    with exif_update:
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
            modify_datetime = st.checkbox(
                "DateTime", value=True, key="bulk_datetime"
            )

    with output_settings:
        # Step 6: Output settings
        st.subheader("5️⃣ Output Settings")

        filename_suffix = st.text_input(
            "Filename Suffix", value="_fixed", key="bulk_suffix"
        )

    process, download = st.columns(2)

    with process:
        # Step 7: Process all
        st.subheader("6️⃣ Process All Images")

        if st.button(
            "🚀 Process All Images", type="primary", use_container_width=True
        ):

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

    with download:
        # Step 8: Download results
        if batch.processed_count > 0:
            st.subheader("7️⃣ Download Results")

            # Create ZIP file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(
                zip_buffer, "w", zipfile.ZIP_DEFLATED
            ) as zip_file:
                for item in batch.get_processed_items():
                    zip_file.writestr(item.output_filename, item.output_bytes)

            zip_buffer.seek(0)

            col1, col2 = st.columns([3, 1])

            with col1:
                st.download_button(
                    label=f"⬇️ Download All ({batch.processed_count} images) as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name=f"fixed_images_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    type="primary",
                    use_container_width=True,
                )

            with col2:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.session_state.batch_processor = None
                    st.rerun()

            # # Summary table
            # st.write("**Processed Images:**")
            # result_data = []
            # for item in batch.get_processed_items():
            #     target = item.get_target_datetime()
            #     result_data.append(
            #         {
            #             "Filename": item.filename,
            #             "Output": item.output_filename,
            #             "Final Date": (
            #                 target.strftime("%Y-%m-%d %H:%M:%S")
            #                 if target
            #                 else "N/A"
            #             ),
            #             "Size": f"{len(item.output_bytes):,} bytes",
            #         }
            #     )

            # df_results = pd.DataFrame(result_data)
            # st.dataframe(df_results, use_container_width=True, hide_index=True)

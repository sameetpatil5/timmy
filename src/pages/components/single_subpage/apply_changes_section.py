import streamlit as st

from utils.exif_writer import (
    update_exif_datetime,
    exif_dict_to_bytes,
    get_modification_summary,
)
from utils.file_exporter import save_image_with_exif, validate_output_bytes
from utils.exif_reader import get_datetime_original


def render_apply_changes_section(
    image,
    file_bytes,
    use_existing_exif,
    target_datetime,
    modify_original,
    modify_digitized,
    modify_datetime,
    output_filename_preview,
    output_bytes,
):

    # Apply changes
    st.subheader("5️⃣ Apply Changes")

    if target_datetime and any([modify_original, modify_digitized, modify_datetime]):

        # Show what will happen
        if use_existing_exif:
            st.info(
                f"ℹ️ **Action:** Preserving existing EXIF date and creating output file with the same datetime."
            )
        else:
            st.info(
                f"ℹ️ **Action:** Updating EXIF date to: **{target_datetime.strftime('%Y-%m-%d %H:%M:%S')}**"
            )

        if st.button("🔧 Apply Changes", type="primary", width="stretch"):

            with st.spinner("Processing image..."):

                # Update EXIF
                exif_dict, exif_error = update_exif_datetime(
                    image,
                    target_datetime,
                    modify_original,
                    modify_digitized,
                    modify_datetime,
                )

                if exif_error:
                    st.error(f"❌ {exif_error}")
                else:
                    # Convert to bytes
                    exif_bytes, bytes_error = exif_dict_to_bytes(exif_dict)

                    if bytes_error:
                        st.error(f"❌ {bytes_error}")
                    else:
                        # Save image with new EXIF
                        output_format = image.format if image.format else "JPEG"

                        output_bytes, save_error = save_image_with_exif(
                            file_bytes, image, exif_bytes, output_format
                        )

                        if save_error:
                            st.error(f"❌ {save_error}")
                        else:
                            # Validate output
                            is_valid_output, validation_warning = validate_output_bytes(
                                len(file_bytes), len(output_bytes)
                            )

                            if not is_valid_output:
                                st.warning(validation_warning)

                            # Store in session state
                            st.session_state.processed_image = output_bytes
                            st.session_state.output_filename = output_filename_preview

                            # Show success
                            st.success("✅ Changes applied successfully!")

                            # Show summary with appropriate message
                            old_dt = get_datetime_original(image)
                            fields_modified = []
                            if modify_original:
                                fields_modified.append("DateTimeOriginal")
                            if modify_digitized:
                                fields_modified.append("DateTimeDigitized")
                            if modify_datetime:
                                fields_modified.append("DateTime")

                            if use_existing_exif:
                                st.info(
                                    f"ℹ️ **Preserved existing EXIF date:** {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
                                )
                                summary = f"**Operation Summary:**\n\n"
                                summary += f"- **Action:** EXIF date preserved (no changes to datetime)\n"
                                summary += f"- **DateTime:** {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"
                                summary += f"- **Fields Verified:** {', '.join(fields_modified)}\n"
                            else:
                                summary = get_modification_summary(
                                    old_dt, target_datetime, fields_modified
                                )

                            st.markdown(summary)

                            # File size info
                            st.info(
                                f"📦 Original: {len(file_bytes):,} bytes → Output: {len(output_bytes):,} bytes"
                            )

    else:
        st.info("👆 Configure the settings above, then click 'Apply Changes'")

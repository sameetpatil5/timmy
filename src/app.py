"""
Streamlit App: Fix Image Capture Date from Filename
Restores correct EXIF datetime metadata based on filename patterns.
"""

import streamlit as st
from datetime import datetime, time
from PIL import Image
import io

# Import utility modules
from config.patterns import SUPPORTED_FORMATS, FILENAME_PATTERNS
from utils.image_loader import load_image, get_image_info, validate_image_format
from utils.exif_reader import get_datetime_original, get_all_datetime_fields
from utils.filename_parser import (
    parse_filename_auto,
    parse_filename_custom,
    get_pattern_examples,
)
from utils.validators import validate_custom_pattern, validate_date
from utils.exif_writer import (
    update_exif_datetime,
    exif_dict_to_bytes,
    get_modification_summary,
)
from utils.file_exporter import (
    save_image_with_exif,
    generate_output_filename,
    validate_output_bytes,
)


# Page configuration
st.set_page_config(page_title="Image EXIF Date Fixer", page_icon="📸", layout="wide")

# App title and description
st.title("📸 Image EXIF Date Fixer")
st.markdown(
    """
Restore the correct capture date for images shared via WhatsApp or other platforms 
that overwrite EXIF metadata. This tool updates the EXIF DateTimeOriginal field 
while preserving image quality.
"""
)

# Initialize session state
if "processed_image" not in st.session_state:
    st.session_state.processed_image = None
if "output_filename" not in st.session_state:
    st.session_state.output_filename = None

# Sidebar for instructions
with st.sidebar:
    st.header("ℹ️ How It Works")
    st.markdown(
        """
    1. **Upload** your image
    2. **Choose** date extraction method:
       - Automatic filename parsing
       - Custom pattern matching
       - Manual date entry
    3. **Select** EXIF fields to update
    4. **Apply** changes
    5. **Download** fixed image
    
    ---
    
    **Supported Formats:** JPG, JPEG, PNG
    
    **Quality Guarantee:** 
    ✅ No compression  
    ✅ No resizing  
    ✅ Original preserved
    """
    )

# Main content
st.header("1️⃣ Upload Image")

uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["jpg", "jpeg", "png"],
    help="Drag and drop or click to browse",
)

if uploaded_file is not None:
    # Read file bytes
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name

    # Validate format
    is_valid_format, format_error = validate_image_format(filename, SUPPORTED_FORMATS)

    if not is_valid_format:
        st.error(format_error)
        st.stop()

    # Load image
    image, load_error = load_image(file_bytes)

    if image is None:
        st.error(f"❌ {load_error}")
        st.stop()

    # Display image and info
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📷 Image Preview")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("📋 Image Information")

        info = get_image_info(image)
        st.write(f"**Filename:** `{filename}`")
        st.write(f"**Format:** {info['format']}")
        st.write(f"**Size:** {info['width']} × {info['height']} pixels")
        st.write(f"**Mode:** {info['mode']}")

        # Display current EXIF dates
        st.write("---")
        st.write("**Current EXIF Dates:**")

        datetime_fields = get_all_datetime_fields(image)

        for field, value in datetime_fields.items():
            if value:
                st.write(f"- {field}: `{value}`")
            else:
                st.write(f"- {field}: *Not set*")

    st.write("---")

    # Date extraction mode selection
    st.header("2️⃣ Choose Date Extraction Method")

    extraction_mode = st.radio(
        "Select how to determine the correct capture date:",
        [
            "🔹 Automatic Filename Parsing",
            "🔹 Custom Filename Pattern",
            "🔹 Manual Date-Time Entry",
        ],
        help="Choose the method that best fits your needs",
    )

    target_datetime = None
    mode_message = ""

    # Mode A: Automatic Parsing
    if extraction_mode == "🔹 Automatic Filename Parsing":
        st.subheader("Automatic Pattern Detection")

        with st.expander("📖 Supported Patterns", expanded=False):
            st.code(get_pattern_examples())

        parsed_dt, confidence, is_ambiguous = parse_filename_auto(filename)

        if parsed_dt:
            st.success(confidence)

            if is_ambiguous:
                st.warning(
                    "⚠️ **Ambiguous Date Detected!** Please verify the date below is correct."
                )

            # Allow user to confirm or modify
            col1, col2 = st.columns(2)

            with col1:
                date_input = st.date_input(
                    "Extracted Date", value=parsed_dt.date(), help="Modify if incorrect"
                )

            with col2:
                time_input = st.time_input(
                    "Time (optional)", value=time(12, 0, 0), help="Default: 12:00:00"
                )

            target_datetime = datetime.combine(date_input, time_input)
            mode_message = f"Using date from filename: {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}"

        else:
            st.error(confidence)
            st.info(
                "💡 Try using **Custom Filename Pattern** or **Manual Entry** instead."
            )

    # Mode B: Custom Pattern
    elif extraction_mode == "🔹 Custom Filename Pattern":
        st.subheader("Define Your Pattern")

        st.markdown(
            """
        Create a pattern using placeholders:
        - `{YYYY}` - 4-digit year
        - `{MM}` - 2-digit month
        - `{DD}` - 2-digit day
        - `{HH}` - 2-digit hour (optional)
        - `{mm}` - 2-digit minute (optional)
        - `{SS}` - 2-digit second (optional)
        """
        )

        custom_pattern = st.text_input(
            "Pattern",
            value="IMG-{YYYY}{MM}{DD}-WA",
            help="Example: IMG-{YYYY}{MM}{DD}-WA for IMG-20241222-WA0135.jpg",
        )

        # Validate pattern
        is_valid_pattern, pattern_error = validate_custom_pattern(custom_pattern)

        if not is_valid_pattern:
            st.error(f"❌ {pattern_error}")
        else:
            # Try to parse
            parsed_dt, parse_message = parse_filename_custom(filename, custom_pattern)

            if parsed_dt:
                st.success(parse_message)

                # Allow modification
                col1, col2 = st.columns(2)

                with col1:
                    date_input = st.date_input("Parsed Date", value=parsed_dt.date())

                with col2:
                    time_input = st.time_input("Parsed Time", value=parsed_dt.time())

                target_datetime = datetime.combine(date_input, time_input)
                mode_message = f"Using custom pattern: {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                st.error(parse_message)

    # Mode C: Manual Entry
    elif extraction_mode == "🔹 Manual Date-Time Entry":
        st.subheader("Manual Date and Time")
        st.warning("⚠️ This will override any date information from the filename.")

        col1, col2 = st.columns(2)

        with col1:
            date_input = st.date_input(
                "Date", value=datetime.now().date(), help="Select the capture date"
            )

        with col2:
            time_input = st.time_input(
                "Time", value=time(12, 0, 0), help="Select the capture time"
            )

        target_datetime = datetime.combine(date_input, time_input)
        mode_message = f"Manually set: {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}"

    st.write("---")

    # Metadata selection
    st.header("3️⃣ Select EXIF Fields to Update")

    col1, col2, col3 = st.columns(3)

    with col1:
        modify_original = st.checkbox(
            "DateTimeOriginal", value=True, help="Primary capture date field"
        )

    with col2:
        modify_digitized = st.checkbox(
            "DateTimeDigitized", value=True, help="Digitization date field"
        )

    with col3:
        modify_datetime = st.checkbox(
            "DateTime", value=True, help="File modification date"
        )

    if not any([modify_original, modify_digitized, modify_datetime]):
        st.warning("⚠️ Please select at least one field to modify.")

    st.write("---")

    # Output settings
    st.header("4️⃣ Output Settings")

    col1, col2 = st.columns(2)

    with col1:
        filename_suffix = st.text_input(
            "Filename Suffix",
            value="_fixed",
            help="Suffix to append to the output filename",
        )

    with col2:
        output_filename_preview = generate_output_filename(filename, filename_suffix)
        st.write(f"**Output filename:** `{output_filename_preview}`")

    st.write("---")

    # Apply changes
    st.header("5️⃣ Apply Changes")

    if target_datetime and any([modify_original, modify_digitized, modify_datetime]):

        if st.button("🔧 Apply Changes", type="primary", use_container_width=True):

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

                            # Show summary
                            old_dt = get_datetime_original(image)
                            fields_modified = []
                            if modify_original:
                                fields_modified.append("DateTimeOriginal")
                            if modify_digitized:
                                fields_modified.append("DateTimeDigitized")
                            if modify_datetime:
                                fields_modified.append("DateTime")

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

    # Download section
    if st.session_state.processed_image:
        st.write("---")
        st.header("6️⃣ Download Fixed Image")

        st.download_button(
            label="⬇️ Download Fixed Image",
            data=st.session_state.processed_image,
            file_name=st.session_state.output_filename,
            mime=f"image/{image.format.lower() if image.format else 'jpeg'}",
            type="primary",
            use_container_width=True,
        )

        st.success("✅ Your image is ready! Click the button above to download.")

else:
    st.info("👆 Upload an image to get started")

    # Show example patterns when no file is uploaded
    with st.expander("📖 Supported Filename Patterns"):
        st.markdown("### Automatically Detected Patterns:")
        for pattern in FILENAME_PATTERNS:
            st.markdown(f"- **{pattern['name']}**: `{pattern['example']}`")

# Footer
st.write("---")
st.markdown(
    """
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>💡 <strong>Quality Guarantee:</strong> No compression • No resizing • Original preserved</p>
    <p>Created with ❤️ for restoring your precious memories</p>
</div>
""",
    unsafe_allow_html=True,
)

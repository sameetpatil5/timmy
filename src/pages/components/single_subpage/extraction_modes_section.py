import streamlit as st
from datetime import datetime, time

from utils.exif_reader import (
    has_valid_exif_datetime,
)
from utils.filename_parser import (
    parse_filename_auto,
    parse_filename_custom,
    get_pattern_examples,
)
from utils.validators import validate_custom_pattern

def render_extraction_modes_section(filename, image, has_exif, exif_dt):
    # Date extraction mode selection
    st.subheader("2️⃣ Choose Date Extraction Method")

    extraction_mode = st.radio(
        "Select how to determine the correct capture date:",
        [
            "Automatic Filename Parsing",
            "Custom Filename Pattern",
            "Manual Date-Time Entry",
        ],
        key="radio_extraction_mode",
        help="Choose the method that best fits your needs. If EXIF date exists, it will be preserved unless Manual Entry is used.",
        label_visibility="collapsed",
        horizontal=True
    )

    target_datetime = None
    mode_message = ""
    use_existing_exif = False

    # If EXIF exists and user is NOT using manual entry, use existing EXIF
    if has_exif and extraction_mode != "Manual Date-Time Entry":
        target_datetime = exif_dt
        use_existing_exif = True
        mode_message = f"Using existing EXIF date: {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        st.success(f"✅ {mode_message}")
        st.info(
            "💡 To override this date, switch to **Manual Date-Time Entry** mode."
        )

    # Mode A: Automatic Parsing (only if no EXIF or user wants to override)
    elif extraction_mode == "Automatic Filename Parsing":

        parsed_dt, confidence, is_ambiguous = parse_filename_auto(filename)

        if parsed_dt:
            st.success(confidence)

            if is_ambiguous:
                st.warning(
                    "⚠️ **Ambiguous Date Detected!** Please verify the date below is correct."
                )

            # Allow user to confirm or modify
            image_preview, image_info = st.columns(2)

            with image_preview:
                date_input = st.date_input(
                    "Extracted Date",
                    value=parsed_dt.date(),
                    help="Modify if incorrect",
                )

            with image_info:
                time_input = st.time_input(
                    "Time (optional)",
                    value=time(12, 0, 0),
                    help="Default: 12:00:00",
                )

            target_datetime = datetime.combine(date_input, time_input)
            mode_message = f"Using date from filename: {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}"

        else:
            st.error(confidence)
            st.info(
                "💡 Try using **Custom Filename Pattern** or **Manual Entry** instead."
            )

    # Mode B: Custom Pattern
    elif extraction_mode == "Custom Filename Pattern":

        custom_pattern_col, pattern_help_col = st.columns([3, 1])

        with custom_pattern_col:
            custom_pattern = st.text_input(
                "Pattern",
                value="IMG-{YYYY}{MM}{DD}-WA",
                help="Example: IMG-{YYYY}{MM}{DD}-WA for IMG-20241222-WA0135.jpg",
                label_visibility="collapsed",
            )

        with pattern_help_col:

            @st.dialog("Create a pattern using placeholders:")
            def show_pattern_docs():
                st.markdown(
                    """
                - `{YYYY}` - 4-digit year
                - `{MM}` - 2-digit month
                - `{DD}` - 2-digit day
                - `{HH}` - 2-digit hour (optional)
                - `{mm}` - 2-digit minute (optional)
                - `{SS}` - 2-digit second (optional)
                """
                )
            
            if st.button("Show Pattern Docs"):
                show_pattern_docs()

        # Validate pattern
        is_valid_pattern, pattern_error = validate_custom_pattern(custom_pattern)

        if not is_valid_pattern:
            st.error(f"❌ {pattern_error}")
        else:
            # Try to parse
            parsed_dt, parse_message = parse_filename_custom(
                filename, custom_pattern
            )

            if parsed_dt:
                st.success(parse_message)

                # Allow modification
                image_preview, image_info = st.columns(2)

                with image_preview:
                    date_input = st.date_input(
                        "Parsed Date", value=parsed_dt.date()
                    )

                with image_info:
                    time_input = st.time_input(
                        "Parsed Time", value=parsed_dt.time()
                    )

                target_datetime = datetime.combine(date_input, time_input)
                mode_message = f"Using custom pattern: {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                st.error(parse_message)

    # Mode C: Manual Entry
    elif extraction_mode == "Manual Date-Time Entry":
        if has_exif:
            st.warning(
                f"⚠️ This will override the existing EXIF date ({exif_dt.strftime('%Y-%m-%d %H:%M:%S')})."
            )
        else:
            st.info("ℹ️ No existing EXIF date found. You can set it manually.")

        image_preview, image_info = st.columns(2)

        # Pre-fill with existing EXIF if available, otherwise use current date
        default_date = exif_dt.date() if has_exif else datetime.now().date()
        default_time = exif_dt.time() if has_exif else time(12, 0, 0)

        with image_preview:
            date_input = st.date_input(
                "Date", value=default_date, help="Select the capture date"
            )

        with image_info:
            time_input = st.time_input(
                "Time", value=default_time, help="Select the capture time"
            )

        target_datetime = datetime.combine(date_input, time_input)
        mode_message = (
            f"Manually set: {target_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        use_existing_exif = False

    return target_datetime, use_existing_exif

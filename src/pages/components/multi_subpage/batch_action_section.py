import streamlit as st
from datetime import datetime, time

from .customize_individual_section import render_customize_individual_section

def render_batch_action_section(batch):

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
        st.warning("⚠️ **Manual Mode:** Sets the SAME date and time for ALL images.")

        col1, col2 = st.columns(2)
        with col1:
            manual_date = st.date_input(
                "Date for all images", value=datetime.now().date()
            )
        with col2:
            manual_time = st.time_input("Time for all images", value=time(12, 0, 0))

        manual_batch_datetime = datetime.combine(manual_date, manual_time)
        batch.set_all_actions("manual", manual_batch_datetime)

        st.success(
            f"✅ Will set all images to: {manual_batch_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    elif batch_action == "Customize Individual Images":
        st.info(
            "💡 Change the action for specific images below. Leave unchanged to use the batch action."
        )
        return True
        # render_customize_individual_section(batch)
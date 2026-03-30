import streamlit as st

from pages.components.footer import show_footer
from pages.components.sidebar import show_sidebar
from pages.single_img_subpage import render_single_image_page
from pages.multi_img_subpage import render_multi_image_page


# Page configuration
st.set_page_config(page_title="Timmy", page_icon="🕛", layout="wide")

show_sidebar()


# App title and description
st.title("🕛 Timmy: reTime your memories")

# Initialize session state
if "processed_image" not in st.session_state:
    st.session_state.processed_image = None
if "output_filename" not in st.session_state:
    st.session_state.output_filename = None
if "batch_processor" not in st.session_state:
    st.session_state.batch_processor = None

st.subheader("1️⃣ Upload Images")

uploaded_files = st.file_uploader(
    "Upload images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    help="Upload single image for detailed analysis OR multiple images for batch processing",
    label_visibility="collapsed",
)

if not uploaded_files:
    # Show instructions
    st.header("Upload an image to get started...")
    st.markdown(
        """
        Once you upload an image, the app will:

        1. Analyze the filename for a valid date
        2. Check if the image has valid EXIF datetime metadata
        3. If not, use the filename extracted date to update the EXIF
        4. Save the fixed image with the updated EXIF metadata
        """
    )

else:
    if len(uploaded_files) > 1:
        # Multi image
        render_multi_image_page(uploaded_files)


    else:
        # Single image
        render_single_image_page(uploaded_files[0])


# Footer
show_footer()

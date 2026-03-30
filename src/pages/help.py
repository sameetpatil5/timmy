import streamlit as st

from pages.components.sidebar import show_sidebar
from pages.components.footer import show_footer

show_sidebar()

# Page configuration
st.set_page_config(page_title="Help", page_icon="❓", layout="wide")

st.header("ℹ️ How It Works")

st.markdown("---")

single_col, multi_col = st.columns(2)

with single_col:
    st.markdown(
        """
        ### Single Image Mode
        1. **Upload** your image
        2. **Choose** date extraction method
        3. **Select** EXIF fields to update
        4. **Apply** changes
        5. **Download** fixed image
    """
    )

with multi_col:
    st.markdown(
        """
        ### Bulk Processing Mode
        1. **Upload** multiple images
        2. **Review** detected dates
        3. **Choose** batch action:
            - Keep existing/extracted dates
            - Use filename for all
            - Set manual date for all
        4. **Customize** individual images (optional)
        5. **Process** all at once
        6. **Download** as ZIP file
    """
    )

show_footer(verbose=True)
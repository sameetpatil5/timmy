import streamlit as st


def show_info():
    st.subheader("🕛 Timmy: reTime your memories")
    st.markdown(
        """
    Restore the correct capture date for images shared via WhatsApp or other platforms 
    that overwrite EXIF metadata. This tool updates the EXIF DateTimeOriginal field 
    while preserving image quality.  

    ---
    """
    )

    st.markdown(
        """    
    **Supported Formats:** JPG, JPEG, PNG
    
    **Quality Guarantee:**  
    ✅ No compression  
    ✅ No resizing  
    ✅ Original preserved

    ---
    """
    )

    st.markdown(
        """
    Upload Images to get Started...
    """
    )

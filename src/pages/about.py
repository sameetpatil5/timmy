import streamlit as st

from pages.components.sidebar import show_sidebar

show_sidebar()


st.set_page_config(
    page_title="About Timmy",
    page_icon="📖",
    layout="wide"
)

st.title("About Timmy")
st.write("Timmy is a tool that restores correct EXIF datetime metadata based on filename patterns.")

st.markdown(
    """
how it works
"""
)

import streamlit as st

from pages.components.info import show_info

def show_sidebar():
    # Sidebar for instructions
    with st.sidebar:
        show_info()
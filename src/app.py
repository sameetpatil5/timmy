import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

home = st.Page("pages/home.py", title="Home", icon="🏠")
about = st.Page("pages/about.py", title="About", icon="📖")
tips = st.Page("pages/tips.py", title="Tips", icon="📚")
help = st.Page("pages/help.py", title="Help", icon="❓")

pg = st.navigation([home, about, tips, help], position="top")

pg.run()

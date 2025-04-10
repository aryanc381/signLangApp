import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Configure page settings
st.set_page_config(
    page_title="Sign Language App",
    page_icon="✋",
    initial_sidebar_state="collapsed"
)

# Remove Streamlit branding
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ✅ Safe auto redirect
if st._is_running_with_streamlit:
    switch_page("signup")

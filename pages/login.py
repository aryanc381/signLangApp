# pages/login.py

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from auth import login_user
import time

# Modern CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
h1 {
    color: #2c3e50;
    text-align: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin-bottom: 30px;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}
.stTextInput>div>div>input {
    border: 2px solid #dfe6e9;
    border-radius: 8px;
    padding: 12px;
    font-size: 16px;
    transition: all 0.3s;
}
.stTextInput>div>div>input:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52,152,219,0.2);
}
.stButton>button {
    background: linear-gradient(to right, #3498db, #2c3e50);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: all 0.3s;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    background: linear-gradient(to right, #2980b9, #1a252f);
}
.css-1v0mbdj {
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    margin: 0 auto;
    max-width: 500px;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.stAlert {
    animation: fadeIn 0.5s ease-in-out;
}
.stAlert .st-at {
    background-color: #ffebee !important;
    color: #c62828 !important;
}
.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    color: #7f8c8d;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    © 2023 Sign Language App | Created with Streamlit
</div>
""", unsafe_allow_html=True)

# Login Form
with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.title("Welcome Back 👋")
        st.markdown("---")

        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Login"):
            if email and password:
                result = login_user(email, password)
                if result["success"]:
                    st.session_state["email"] = email
                    st.success("Login successful! Redirecting...")
                    time.sleep(2)
                    switch_page("home")
                else:
                    st.error(f"Login failed: {result['error']}")
            else:
                st.error("Please fill in both fields.")

        st.markdown("---")
        st.markdown("New here?")
        if st.button("Sign Up Instead"):
            switch_page("signup")

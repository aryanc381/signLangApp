import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page
from firebase_config import db, WEB_API_KEY
import time
from firebase_admin import firestore

# Custom CSS
st.markdown("""
<style>
/* Main container styling */
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

# Footer
st.markdown("""
<div class="footer">
    © 2023 Sign Language App | Created with Streamlit
</div>
""", unsafe_allow_html=True)

# Store user info in Firestore
def store_user_data(uid, email):
    db.collection("users").document(uid).set({
        "email": email,
        "created_at": firestore.SERVER_TIMESTAMP
    })

# Firebase Sign-Up Endpoint
FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={WEB_API_KEY}"

with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.title("Create Your Account")
        st.markdown("---")
        
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Create Password", type="password", placeholder="Choose a strong password")

        if st.button("Sign Up", key="signup_button"):
            if email and password:
                payload = {
                    "email": email,
                    "password": password,
                    "returnSecureToken": True
                }
                try:
                    response = requests.post(FIREBASE_SIGNUP_URL, json=payload)
                    result = response.json()

                    if "error" in result:
                        error_msg = result["error"]["message"].replace("_", " ").capitalize()
                        st.error(f"Signup failed: {error_msg}")
                    else:
                        uid = result["localId"]
                        store_user_data(uid, email)
                        st.success("✅ Account created successfully! Redirecting to login...")
                        st.session_state.signup_complete = True

                except Exception as e:
                    st.error(f"Signup failed: {e}")
            else:
                st.error("Please fill in both fields to continue")

        st.markdown("---")
        st.markdown("Already have an account?")
        if st.button("Login Instead", key="login_button"):
            switch_page("login")

if st.session_state.get('signup_complete', False):
    time.sleep(2)
    switch_page("login")

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set page configuration
st.set_page_config(page_title="Home", layout="centered")

# Enhanced CSS styling (keeping your original structure)
st.markdown("""
<style>
/* Main container styling */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Title styling */
h1 {
    color: #2c3e50;
    text-align: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin-bottom: 30px;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
}

/* Card container */
.stContainer {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    margin: 0 auto;
    max-width: 600px;
}

/* Role selection styling */
.role-option {
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.role-option:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.1);
}

.interviewer-option {
    background-color: rgba(52, 152, 219, 0.1);
    border-color: #3498db;
}

.interviewee-option {
    background-color: rgba(46, 204, 113, 0.1);
    border-color: #2ecc71;
}

.role-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    text-align: center;
}

.role-desc {
    color: #7f8c8d;
    font-size: 0.9rem;
    text-align: center;
}

/* Button styling */
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
    margin-top: 20px;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    background: linear-gradient(to right, #2980b9, #1a252f);
}

/* Footer styling */
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

# Check if user is logged in
if "username" not in st.session_state:
    st.warning("Please log in first.")
    switch_page("login")

# Main content
with st.container():
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.title("Welcome to the Inclusive Interview Platform 👋")
        
        st.markdown("""
        <div style='text-align: center; color: #2c3e50; margin-bottom: 30px;'>
            Bridging communication gaps between interviewers and deaf/mute candidates
        </div>
        """, unsafe_allow_html=True)
        
        # Role selection using radio buttons with custom styling
        st.markdown("<h3 style='text-align: center; margin-bottom: 1.5rem;'>Select Your Role</h3>", 
                   unsafe_allow_html=True)
        
        # Interviewer option
        with st.container():
            st.markdown("""
            <div class="role-option interviewer-option">
                <div class="role-title">👔 Interviewer</div>
                <div class="role-desc">I will be conducting the interview</div>
            </div>
            """, unsafe_allow_html=True)
            interviewer_btn = st.button("Select Interviewer", key="interviewer_btn")
        
        # Interviewee option
        with st.container():
            st.markdown("""
            <div class="role-option interviewee-option">
                <div class="role-title">👤 Interviewee</div>
                <div class="role-desc">I will be participating in the interview</div>
            </div>
            """, unsafe_allow_html=True)
            interviewee_btn = st.button("Select Interviewee", key="interviewee_btn")
        
        # Handle role selection
        if interviewer_btn:
            st.session_state.role = "interviewer"
            switch_page("voice")
        elif interviewee_btn:
            st.session_state.role = "interviewee"
            switch_page("signlang_chat")

# Add footer
st.markdown("""
<div class="footer">
    © 2023 Inclusive Interview Platform | Created with Streamlit
</div>
""", unsafe_allow_html=True) 
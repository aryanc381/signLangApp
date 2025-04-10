import streamlit as st
from streamlit_extras.stylable_container import stylable_container

# Page configuration
st.set_page_config(
    page_title="About Us | Interview Platform",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Check if user is logged in
if "username" not in st.session_state:
    st.warning("Please login to access this page.")
    st.stop()

# Initialize current_page in session state if not exists
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'about'

# Custom CSS with improved button contrast
st.markdown("""
<style>
/* Main container */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Ensure all text is visible */
body, p, h1, h2, h3, h4, h5, h6, div, span {
    color: #2c3e50 !important;
}

/* Navigation bar */
.navbar {
    display: flex;
    justify-content: center;
    gap: 1rem;
    padding: 1rem;
    margin-bottom: 2rem;
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Navigation buttons with better contrast */
.stButton>button {
    border: none !important;
    background: none !important;
    color: #2c3e50 !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    border-radius: 8px !important;
    transition: all 0.3s !important;
    cursor: pointer !important;
    font-size: 1rem !important;
    margin: 0 !important;
}

.stButton>button:hover {
    background-color: rgba(52, 152, 219, 0.1) !important;
    transform: translateY(-2px) !important;
}

.stButton>button:disabled {
    background: linear-gradient(to right, #3498db, #2c3e50) !important;
    color: white !important;
    transform: none !important;
}

/* Content cards */
.content-card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

/* Title styling */
h1 {
    color: #2c3e50;
    text-align: center;
    margin-bottom: 1.5rem;
}

/* Footer */
.footer {
    text-align: center;
    padding: 1.5rem;
    color: #7f8c8d !important;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Navigation system - fixed to avoid rerun in callback
def change_page(page):
    st.session_state.current_page = page

# Navigation bar - using columns for layout
with st.container():
    cols = st.columns(4)
    
    with cols[0]:
        st.button("About Us", 
                key="nav_about", 
                on_click=change_page, 
                args=('about',),
                disabled=(st.session_state.current_page == 'about'))
    
    with cols[1]:
        st.button("FAQ", 
                key="nav_faq",
                on_click=change_page, 
                args=('faq',),
                disabled=(st.session_state.current_page == 'faq'))
    
    with cols[2]:
        st.button("Blog", 
                key="nav_blog",
                on_click=change_page, 
                args=('blog',),
                disabled=(st.session_state.current_page == 'blog'))
    
    with cols[3]:
        st.button("Support", 
                key="nav_support",
                on_click=change_page, 
                args=('support',),
                disabled=(st.session_state.current_page == 'support'))

# Page content
if st.session_state.current_page == 'about':
    with stylable_container(
        "content-card",
        css_styles="""
            {
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }
        """
    ):
        st.title("About Us")
        st.markdown("""
        ### Our Mission
        We're dedicated to creating inclusive interview experiences for everyone, 
        especially focusing on accessibility for deaf and mute candidates.
        
        ### Our Team
        - **Aryan Chauhan**
        - **Atharva Gujar**
        - **Abdulqadir Kayamkhani**
        - **Mandar Gade**
        
        ### Technology
        Using cutting-edge speech recognition and sign language interpretation 
        to bridge communication gaps in professional settings.
        """)

elif st.session_state.current_page == 'faq':
    with stylable_container(
        "content-card",
        css_styles="""
            {
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }
        """
    ):
        st.title("Frequently Asked Questions")
        with st.expander("How does the voice-to-text feature work?"):
            st.markdown("Our system uses advanced speech recognition algorithms to convert spoken words into text in real-time with 95% accuracy.")
        with st.expander("Is there a limit to recording duration?"):
            st.markdown("Currently, we support recordings up to 5 minutes for optimal performance. For longer interviews, please contact support.")
        with st.expander("Is my interview data secure?"):
            st.markdown("Yes, all interview data is encrypted and stored securely. We comply with GDPR and other privacy regulations.")
        with st.expander("What browsers are supported?"):
            st.markdown("Our platform works best on Chrome, Firefox, and Edge. Safari support is coming soon.")
        with st.expander("How do I reset my password?"):
            st.markdown("Click on 'Forgot Password' on the login page and follow the instructions sent to your registered email.")
        with st.expander("Can I practice interviews before the real one?"):
            st.markdown("Yes! We offer a practice mode with sample questions to help you prepare.")

elif st.session_state.current_page == 'blog':
    with stylable_container(
        "content-card",
        css_styles="""
            {
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }
        """
    ):
        st.title("Latest Blog Posts")
        st.markdown("""
        ### The Future of Inclusive Hiring: 2023 Trends
        Explore how companies are adapting their hiring processes to be more accessible...
        
        ### How AI is Revolutionizing Interview Accessibility
        Learn about our breakthrough technology helping candidates with disabilities...
        
        ### Case Study: Improving Interview Success Rates by 40%
        See how our platform helped a Fortune 500 company improve their hiring outcomes...
        
        ### Upcoming Features Sneak Peek
        Get a first look at the new features we're launching next quarter...
        """)

elif st.session_state.current_page == 'support':
    with stylable_container(
        "content-card",
        css_styles="""
            {
                background: white;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }
        """
    ):
        st.title("Support Center")
        st.markdown("""
        ### Contact Us
        **Email:** 1032222560@mitwpu.edu.in  
        **Phone:** +91 8087376252  
        **Address:** Paud Road, Kothrud, MIT-WPU, Pune, India  
        
        **Support Hours:**  
        Monday-Friday: 9:00 AM - 6:00 PM IST  
        Saturday: 10:00 AM - 2:00 PM IST  
        Sunday: Closed
        """)

# Footer
st.markdown("""
<div class="footer">
    © 2023 Inclusive Interview Platform | All Rights Reserved
</div>
""", unsafe_allow_html=True)
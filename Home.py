import streamlit as st
import json
from datetime import datetime

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Hardcoded credentials (in a real application, this should be more secure)
VALID_EMAIL = "admin@arosefinance.co.uk"
VALID_PASSWORD = "finance2025"

# Read version info
def get_version_info():
    try:
        with open('config/version.json', 'r') as f:
            version_data = json.load(f)
            return version_data['version'], version_data['last_updated']
    except Exception as e:
        return "1.0.0", datetime.now().strftime("%Y-%m-%d")

def login():
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False

# Custom CSS to hide sidebar when not logged in
def local_css():
    style = """
    <style>
    #MainMenu {visibility: hidden;}
    .stSidebar {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    if not st.session_state.logged_in:
        st.markdown(style, unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="Arose Finance - Loan Origination System",
    page_icon="💰",
    layout="wide"
)

# Apply custom CSS
local_css()

# Login form if not logged in
if not st.session_state.logged_in:
    st.title("Welcome to Arose Finance")
    st.subheader("Loan Origination System")
    version, last_updated = get_version_info()
    st.caption(f"Version {version} (Last updated: {last_updated})")
    st.subheader("Please login to continue")
    
    # Add demo login button
    if st.button("Demo Login (Skip Form)"):
        login()
        st.rerun()
    
    with st.form("login_form"):
        email = st.text_input("Email", value="admin@arosefinance.co.uk")
        password = st.text_input("Password", type="password", value="finance2025")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if email == VALID_EMAIL and password == VALID_PASSWORD:
                login()
                st.rerun()
            else:
                st.error("Invalid credentials")

# Main content when logged in
else:
    # Add logout button in sidebar
    with st.sidebar:
        if st.button("Logout"):
            logout()
            st.rerun()
        st.success("Select a workflow step above.")

    st.title("Arose Finance - Loan Origination System")
    version, last_updated = get_version_info()
    st.caption(f"Version {version} (Last updated: {last_updated})")

    st.markdown("""
    ## Welcome to the Arose Finance Loan Origination System

    This application guides you through the complete loan origination process, from initial call transcript to client communication with loan offers.

    ### Workflow Steps:

    1. **Initial Call Transcript** - Record initial call information, capture question set responses, and pre-populate fact-find
    2. **Document Collection Form** - Collect client documents and answers via form to pre-populate fact-find
    3. **Fact-Find Completion** - Complete the fact-find with client during the scheduled meeting
    4. **Broker Verification** - Verify and approve the transcoded client profile
    5. **Lender Matching** - Match the transcoded client profile to lenders with probability of success
    6. **Algorithm Learning** - Algorithm self-educates based on loan outcomes and feedback
    7. **Lender Communication** - Send bespoke emails to lenders and collect their feedback
    8. **Client Communication** - Present lender feedback to client and send templated email

    ### Getting Started

    Navigate through the workflow using the sidebar menu. Each step will guide you through the required information and actions.

    For assistance, please contact support@arosefinance.com
    """) 
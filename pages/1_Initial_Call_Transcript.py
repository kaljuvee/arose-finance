import streamlit as st
import pandas as pd
from datetime import date, datetime

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

st.set_page_config(
    page_title="Initial Call Transcript",
    page_icon="📞",
    layout="wide"
)

st.title("Step 1: Initial Call Transcript")
st.markdown("Record initial call information, capture question set responses, and pre-populate fact-find")

# Add demo data checkbox
use_demo_data = st.sidebar.checkbox("Use Demo Data", value=False, key="use_demo_data_step1")

# Initialize session state for storing application data
if 'application_data' not in st.session_state:
    st.session_state.application_data = {
        'initial_call': {},
        'question_set': {},
        'personal_info': {},
        'loan_info': {},
        'follow_up': {}
    }

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Call Information", "Initial Question Set", "Client Information", "Follow-up Actions"])

# Generate demo data if checkbox is checked
if use_demo_data:
    # Demo data for Call Information
    demo_call_date = date.today()
    demo_call_time = datetime.now().time()
    demo_call_duration = 30
    demo_call_source = "8x8 Work (PC)"
    demo_broker_name = "John Smith"
    demo_call_notes = "Client is looking to purchase a new home. They have good credit and stable income. Interested in a 30-year fixed rate mortgage."
    
    # Demo data for Initial Question Set
    demo_loan_purpose = "Home Purchase"
    demo_property_type = "Single Family Home"
    demo_property_use = "Primary Residence"
    demo_loan_amount_range = "$250,000-$500,000"
    demo_credit_score_range = "700-750"
    demo_income_type = ["W2 Employment", "Investment Income"]
    
    # Demo data for Client Information
    demo_first_name = "Michael"
    demo_last_name = "Johnson"
    demo_email = "michael.johnson@example.com"
    demo_phone = "(555) 123-4567"
    demo_preferred_contact = "Email"
    demo_best_time = "Evening"
    
    # Demo data for Follow-up Actions
    demo_meeting_date = date.today() + pd.Timedelta(days=7)
    demo_meeting_time = datetime.strptime("14:00", "%H:%M").time()
    demo_meeting_type = "Video Call (Zoom)"
    demo_docs_to_request = ["ID/Passport", "Proof of Address", "Bank Statements (3 months)", "Pay Stubs (2 months)", "Tax Returns (2 years)"]
    demo_additional_info = "Please bring information about any existing debts and current mortgage statements if applicable."

with tab1:
    st.header("Call Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        call_date = st.date_input("Call Date", value=demo_call_date if use_demo_data else date.today(), key="call_date")
        call_time = st.time_input("Call Time", value=demo_call_time if use_demo_data else datetime.now().time(), key="call_time")
        call_duration = st.number_input("Call Duration (minutes)", min_value=1, value=demo_call_duration if use_demo_data else 15, step=1, key="call_duration")
    
    with col2:
        call_source = st.selectbox(
            "Call Source",
            ["8x8 Work (PC)", "8x8 Work (Mobile)", "Teams", "Zoom", "Cellular Mobile"],
            index=0 if use_demo_data else 0,
            key="call_source"
        )
        broker_name = st.text_input("Broker Name", value=demo_broker_name if use_demo_data else "", key="broker_name")
        call_notes = st.text_area("Call Notes", value=demo_call_notes if use_demo_data else "", height=100, key="call_notes")
    
    # Upload call transcript
    st.subheader("Call Transcript")
    transcript_file = st.file_uploader("Upload Call Transcript", type=["txt", "pdf", "docx"], key="transcript_file")
    
    if transcript_file is not None:
        st.success(f"Transcript uploaded: {transcript_file.name}")
        # In a real implementation, we would process the transcript here
        st.text_area("Transcript Preview (Auto-Generated)", 
                    "This is a placeholder for the transcript content that would be extracted from the uploaded file.",
                    height=150, key="transcript_preview")
    elif use_demo_data:
        st.info("Demo transcript: A simulated transcript would be available here in a real implementation.")

with tab2:
    st.header("Initial Question Set")
    
    st.info("These questions help determine the client's needs and pre-populate the fact-find form.")
    
    # Loan Purpose Questions
    st.subheader("Loan Purpose")
    loan_purpose = st.selectbox(
        "What is the primary purpose of this loan?",
        ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation", "Business", "Other"],
        index=0 if use_demo_data else 0,
        key="loan_purpose"
    )
    
    if loan_purpose == "Other":
        other_purpose = st.text_input("Please specify purpose", key="other_purpose")
    
    # Property Questions
    st.subheader("Property Information")
    property_type = st.selectbox(
        "What type of property are you looking to finance?",
        ["Single Family Home", "Multi-Family Home", "Condominium", "Townhouse", "Commercial Property", "Land"],
        index=0 if use_demo_data else 0,
        key="property_type"
    )
    
    property_use = st.selectbox(
        "How will the property be used?",
        ["Primary Residence", "Secondary/Vacation Home", "Investment Property", "Business"],
        index=0 if use_demo_data else 0,
        key="property_use"
    )
    
    # Financial Questions
    st.subheader("Financial Overview")
    loan_amount_range = st.select_slider(
        "Approximate loan amount needed",
        options=["$50,000-$100,000", "$100,000-$250,000", "$250,000-$500,000", "$500,000-$1,000,000", "Over $1,000,000"],
        value=demo_loan_amount_range if use_demo_data else "$100,000-$250,000",
        key="loan_amount_range"
    )
    
    credit_score_range = st.select_slider(
        "Approximate credit score range",
        options=["Below 600", "600-650", "650-700", "700-750", "750+", "Unsure"],
        value=demo_credit_score_range if use_demo_data else "Unsure",
        key="credit_score_range"
    )
    
    income_type = st.multiselect(
        "What type(s) of income do you have?",
        ["W2 Employment", "Self-Employment", "Rental Income", "Investment Income", "Retirement", "Other"],
        default=demo_income_type if use_demo_data else [],
        key="income_type"
    )

with tab3:
    st.header("Client Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name", value=demo_first_name if use_demo_data else "", key="first_name")
        last_name = st.text_input("Last Name", value=demo_last_name if use_demo_data else "", key="last_name")
        email = st.text_input("Email Address", value=demo_email if use_demo_data else "", key="email")
    
    with col2:
        phone = st.text_input("Phone Number", value=demo_phone if use_demo_data else "", key="phone")
        preferred_contact = st.selectbox(
            "Preferred Contact Method",
            ["Email", "Phone", "Text"],
            index=0 if use_demo_data else 0,
            key="preferred_contact"
        )
        best_time = st.selectbox(
            "Best Time to Contact",
            ["Morning", "Afternoon", "Evening", "Anytime"],
            index=2 if use_demo_data else 3,
            key="best_time"
        )

with tab4:
    st.header("Follow-up Actions")
    
    st.subheader("Schedule Fact-Find Meeting")
    meeting_date = st.date_input("Meeting Date", value=demo_meeting_date if use_demo_data else date.today() + pd.Timedelta(days=7), key="meeting_date")
    meeting_time = st.time_input("Meeting Time", value=demo_meeting_time if use_demo_data else datetime.now().time(), key="meeting_time")
    meeting_type = st.selectbox(
        "Meeting Type",
        ["In-Person", "Video Call (Teams)", "Video Call (Zoom)", "Phone Call"],
        index=2 if use_demo_data else 0,
        key="meeting_type"
    )
    
    st.subheader("Form and Documentation")
    st.markdown("Select documents to request from client:")
    
    docs_to_request = st.multiselect(
        "Required Documents",
        ["ID/Passport", "Proof of Address", "Bank Statements (3 months)", "Pay Stubs (2 months)", 
         "Tax Returns (2 years)", "W-2 Forms", "1099 Forms", "Business Financial Statements",
         "Property Information", "Existing Mortgage Statement"],
        default=demo_docs_to_request if use_demo_data else ["ID/Passport", "Proof of Address", "Bank Statements (3 months)"],
        key="docs_to_request"
    )
    
    additional_info = st.text_area("Additional Information to Request", value=demo_additional_info if use_demo_data else "", key="additional_info")

# Save application data
if st.button("Save and Continue"):
    # Update session state with form data
    # Call Information
    st.session_state.application_data['initial_call'] = {
        'call_date': call_date.strftime("%Y-%m-%d") if call_date else None,
        'call_time': call_time.strftime("%H:%M") if call_time else None,
        'call_duration': call_duration,
        'call_source': call_source,
        'broker_name': broker_name,
        'call_notes': call_notes,
        'transcript_file': transcript_file.name if transcript_file else None
    }
    
    # Question Set
    st.session_state.application_data['question_set'] = {
        'loan_purpose': loan_purpose,
        'property_type': property_type,
        'property_use': property_use,
        'loan_amount_range': loan_amount_range,
        'credit_score_range': credit_score_range,
        'income_type': income_type
    }
    
    # Personal Info
    st.session_state.application_data['personal_info'] = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'preferred_contact': preferred_contact,
        'best_time': best_time
    }
    
    # Follow-up
    st.session_state.application_data['follow_up'] = {
        'meeting_date': meeting_date.strftime("%Y-%m-%d") if meeting_date else None,
        'meeting_time': meeting_time.strftime("%H:%M") if meeting_time else None,
        'meeting_type': meeting_type,
        'docs_to_request': docs_to_request,
        'additional_info': additional_info
    }
    
    # Generate outputs
    st.session_state.outputs = {
        'form_generated': True,
        'follow_up_email': True,
        'meeting_invite': True,
        'fact_find_prepopulated': True
    }
    
    st.success("Initial call information saved successfully! Follow-up form and correspondence will be generated.")
    
    # Display outputs
    st.subheader("Outputs Generated")
    st.markdown("✅ Bespoke client form created")
    st.markdown("✅ Follow-up correspondence drafted")
    st.markdown("✅ Meeting invite prepared")
    st.markdown("✅ Fact-find pre-populated with available information")
    
    st.balloons() 
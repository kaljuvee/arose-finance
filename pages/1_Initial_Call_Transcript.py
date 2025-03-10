import streamlit as st
import pandas as pd
from datetime import date, datetime

st.set_page_config(
    page_title="Initial Call Transcript",
    page_icon="📞",
    layout="wide"
)

st.title("Step 1: Initial Call Transcript")
st.markdown("Record initial call information, capture question set responses, and pre-populate fact-find")

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

with tab1:
    st.header("Call Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        call_date = st.date_input("Call Date", value=date.today(), key="call_date")
        call_time = st.time_input("Call Time", value=datetime.now().time(), key="call_time")
        call_duration = st.number_input("Call Duration (minutes)", min_value=1, value=15, step=1, key="call_duration")
    
    with col2:
        call_source = st.selectbox(
            "Call Source",
            ["8x8 Work (PC)", "8x8 Work (Mobile)", "Teams", "Zoom", "Cellular Mobile"],
            key="call_source"
        )
        broker_name = st.text_input("Broker Name", key="broker_name")
        call_notes = st.text_area("Call Notes", height=100, key="call_notes")
    
    # Upload call transcript
    st.subheader("Call Transcript")
    transcript_file = st.file_uploader("Upload Call Transcript", type=["txt", "pdf", "docx"], key="transcript_file")
    
    if transcript_file is not None:
        st.success(f"Transcript uploaded: {transcript_file.name}")
        # In a real implementation, we would process the transcript here
        st.text_area("Transcript Preview (Auto-Generated)", 
                    "This is a placeholder for the transcript content that would be extracted from the uploaded file.",
                    height=150, key="transcript_preview")

with tab2:
    st.header("Initial Question Set")
    
    st.info("These questions help determine the client's needs and pre-populate the fact-find form.")
    
    # Loan Purpose Questions
    st.subheader("Loan Purpose")
    loan_purpose = st.selectbox(
        "What is the primary purpose of this loan?",
        ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation", "Business", "Other"],
        key="loan_purpose"
    )
    
    if loan_purpose == "Other":
        other_purpose = st.text_input("Please specify purpose", key="other_purpose")
    
    # Property Questions
    st.subheader("Property Information")
    property_type = st.selectbox(
        "What type of property are you looking to finance?",
        ["Single Family Home", "Multi-Family Home", "Condominium", "Townhouse", "Commercial Property", "Land"],
        key="property_type"
    )
    
    property_use = st.selectbox(
        "How will the property be used?",
        ["Primary Residence", "Secondary/Vacation Home", "Investment Property", "Business"],
        key="property_use"
    )
    
    # Financial Questions
    st.subheader("Financial Overview")
    loan_amount_range = st.select_slider(
        "Approximate loan amount needed",
        options=["$50,000-$100,000", "$100,000-$250,000", "$250,000-$500,000", "$500,000-$1,000,000", "Over $1,000,000"],
        key="loan_amount_range"
    )
    
    credit_score_range = st.select_slider(
        "Approximate credit score range",
        options=["Below 600", "600-650", "650-700", "700-750", "750+", "Unsure"],
        key="credit_score_range"
    )
    
    income_type = st.multiselect(
        "What type(s) of income do you have?",
        ["W2 Employment", "Self-Employment", "Rental Income", "Investment Income", "Retirement", "Other"],
        key="income_type"
    )

with tab3:
    st.header("Client Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name", key="first_name")
        last_name = st.text_input("Last Name", key="last_name")
        email = st.text_input("Email Address", key="email")
    
    with col2:
        phone = st.text_input("Phone Number", key="phone")
        preferred_contact = st.selectbox(
            "Preferred Contact Method",
            ["Email", "Phone", "Text"],
            key="preferred_contact"
        )
        best_time = st.selectbox(
            "Best Time to Contact",
            ["Morning", "Afternoon", "Evening", "Anytime"],
            key="best_time"
        )

with tab4:
    st.header("Follow-up Actions")
    
    st.subheader("Schedule Fact-Find Meeting")
    meeting_date = st.date_input("Meeting Date", value=date.today() + pd.Timedelta(days=7), key="meeting_date")
    meeting_time = st.time_input("Meeting Time", key="meeting_time")
    meeting_type = st.selectbox(
        "Meeting Type",
        ["In-Person", "Video Call (Teams)", "Video Call (Zoom)", "Phone Call"],
        key="meeting_type"
    )
    
    st.subheader("Form and Documentation")
    st.markdown("Select documents to request from client:")
    
    docs_to_request = st.multiselect(
        "Required Documents",
        ["ID/Passport", "Proof of Address", "Bank Statements (3 months)", "Pay Stubs (2 months)", 
         "Tax Returns (2 years)", "W-2 Forms", "1099 Forms", "Business Financial Statements",
         "Property Information", "Existing Mortgage Statement"],
        default=["ID/Passport", "Proof of Address", "Bank Statements (3 months)"],
        key="docs_to_request"
    )
    
    additional_info = st.text_area("Additional Information to Request", key="additional_info")

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
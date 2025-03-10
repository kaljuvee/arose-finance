import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime, timedelta

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

st.set_page_config(
    page_title="Fact-Find Completion",
    page_icon="📋",
    layout="wide"
)

st.title("Step 3: Fact-Find Completion")
st.markdown("Complete the fact-find with client during the scheduled meeting")

# Check if previous steps are completed
if 'application_data' not in st.session_state or 'form_responses' not in st.session_state:
    st.warning("Please complete Steps 1 and 2 first.")
    st.stop()

# Initialize session state for fact-find data
if 'fact_find_data' not in st.session_state:
    st.session_state.fact_find_data = {
        'meeting_details': {},
        'client_profile': {},
        'property_details': {},
        'financial_situation': {},
        'loan_requirements': {},
        'risk_profile': {},
        'additional_notes': {}
    }

# Create tabs for different sections of the fact-find
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Meeting Details", 
    "Client Profile", 
    "Property & Loan Details", 
    "Financial Situation", 
    "Risk Profile"
])

with tab1:
    st.header("Meeting Details")
    
    # Pre-populate with data from previous steps
    follow_up = st.session_state.application_data.get('follow_up', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        meeting_date = st.date_input(
            "Meeting Date", 
            value=datetime.strptime(follow_up.get('meeting_date', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d") if follow_up.get('meeting_date') else datetime.now(),
            key="meeting_date"
        )
        meeting_time = st.time_input(
            "Meeting Time",
            key="meeting_time"
        )
        meeting_duration = st.number_input("Meeting Duration (minutes)", min_value=15, value=60, step=15, key="meeting_duration")
    
    with col2:
        meeting_type = st.selectbox(
            "Meeting Type",
            ["In-Person", "Video Call (Teams)", "Video Call (Zoom)", "Phone Call"],
            index=["In-Person", "Video Call (Teams)", "Video Call (Zoom)", "Phone Call"].index(follow_up.get('meeting_type', "In-Person")) if follow_up.get('meeting_type') else 0,
            key="meeting_type"
        )
        broker_name = st.text_input("Broker Name", key="broker_name")
        meeting_notes = st.text_area("Meeting Notes", height=100, key="meeting_notes")
    
    # Upload meeting transcript
    st.subheader("Meeting Transcript")
    transcript_file = st.file_uploader("Upload Meeting Transcript", type=["txt", "pdf", "docx"], key="meeting_transcript")
    
    if transcript_file is not None:
        st.success(f"Transcript uploaded: {transcript_file.name}")
        # In a real implementation, we would process the transcript here
        st.text_area("Transcript Preview (Auto-Generated)", 
                    "This is a placeholder for the transcript content that would be extracted from the uploaded file.",
                    height=150, key="meeting_transcript_preview")

with tab2:
    st.header("Client Profile")
    st.info("This section is pre-populated with information from previous steps. Please verify and complete any missing information.")
    
    # Pre-populate with data from previous steps
    personal_info = st.session_state.application_data.get('personal_info', {})
    form_personal = st.session_state.form_responses.get('personal_details', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input(
            "First Name", 
            value=form_personal.get('first_name', personal_info.get('first_name', '')),
            key="ff_first_name"
        )
        last_name = st.text_input(
            "Last Name", 
            value=form_personal.get('last_name', personal_info.get('last_name', '')),
            key="ff_last_name"
        )
        dob = st.date_input(
            "Date of Birth", 
            value=datetime.strptime(form_personal.get('dob', '1980-01-01'), "%Y-%m-%d") if form_personal.get('dob') else datetime.now(),
            key="ff_dob"
        )
        marital_status = st.selectbox(
            "Marital Status",
            ["Single", "Married", "Civil Partnership", "Divorced", "Widowed", "Separated"],
            index=["Single", "Married", "Civil Partnership", "Divorced", "Widowed", "Separated"].index(form_personal.get('marital_status', "Single")) if form_personal.get('marital_status') else 0,
            key="ff_marital_status"
        )
    
    with col2:
        email = st.text_input(
            "Email Address", 
            value=form_personal.get('email', personal_info.get('email', '')),
            key="ff_email"
        )
        phone = st.text_input(
            "Phone Number", 
            value=form_personal.get('phone', personal_info.get('phone', '')),
            key="ff_phone"
        )
        address = st.text_area(
            "Current Address", 
            value=form_personal.get('address', ''),
            key="ff_address"
        )
        years_at_address = st.number_input(
            "Years at Current Address", 
            min_value=0.0, 
            value=float(form_personal.get('years_at_address', 0)),
            step=0.5, 
            key="ff_years_at_address"
        )
    
    # Dependents
    st.subheader("Dependents")
    has_dependents = st.checkbox("Client has dependents", key="has_dependents")
    
    if has_dependents:
        num_dependents = st.number_input("Number of Dependents", min_value=1, max_value=10, value=1, step=1, key="num_dependents")
        dependent_ages = st.text_input("Ages of Dependents (comma separated)", key="dependent_ages")

with tab3:
    st.header("Property & Loan Details")
    
    # Pre-populate with data from previous steps
    property_details = st.session_state.form_responses.get('property_details', {})
    financial_details = st.session_state.form_responses.get('financial_details', {})
    question_set = st.session_state.application_data.get('question_set', {})
    
    # Property Details
    st.subheader("Property Details")
    col1, col2 = st.columns(2)
    
    with col1:
        property_type = st.selectbox(
            "Property Type",
            ["Single Family Home", "Multi-Family Home", "Condominium", "Townhouse", "Commercial Property", "Land"],
            index=["Single Family Home", "Multi-Family Home", "Condominium", "Townhouse", "Commercial Property", "Land"].index(property_details.get('property_type', question_set.get('property_type', "Single Family Home"))) if property_details.get('property_type') or question_set.get('property_type') else 0,
            key="ff_property_type"
        )
        property_value = st.number_input(
            "Estimated Property Value ($)", 
            min_value=0, 
            value=int(property_details.get('property_value', 0)),
            step=10000, 
            key="ff_property_value"
        )
        property_age = st.number_input("Property Age (years)", min_value=0, value=0, step=1, key="ff_property_age")
        
    with col2:
        property_use = st.selectbox(
            "Property Use",
            ["Primary Residence", "Secondary/Vacation Home", "Investment Property", "Business"],
            index=["Primary Residence", "Secondary/Vacation Home", "Investment Property", "Business"].index(property_details.get('property_use', question_set.get('property_use', "Primary Residence"))) if property_details.get('property_use') or question_set.get('property_use') else 0,
            key="ff_property_use"
        )
        property_address = st.text_area(
            "Property Address", 
            value=property_details.get('property_address', ''),
            key="ff_property_address"
        )
        property_condition = st.selectbox(
            "Property Condition",
            ["Excellent", "Good", "Fair", "Poor", "Needs Renovation"],
            key="ff_property_condition"
        )
    
    # Loan Details
    st.subheader("Loan Requirements")
    col1, col2 = st.columns(2)
    
    with col1:
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation", "Business", "Other"],
            index=["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation", "Business", "Other"].index(financial_details.get('loan_purpose', question_set.get('loan_purpose', "Home Purchase"))) if financial_details.get('loan_purpose') or question_set.get('loan_purpose') else 0,
            key="ff_loan_purpose"
        )
        loan_amount = st.number_input(
            "Requested Loan Amount ($)", 
            min_value=0, 
            value=int(financial_details.get('loan_amount', 0)),
            step=10000, 
            key="ff_loan_amount"
        )
        down_payment = st.number_input(
            "Down Payment Amount ($)", 
            min_value=0, 
            value=int(financial_details.get('down_payment', 0)),
            step=5000, 
            key="ff_down_payment"
        )
        
    with col2:
        loan_term_preference = st.selectbox(
            "Preferred Loan Term",
            ["15 years", "20 years", "25 years", "30 years", "Other"],
            key="ff_loan_term"
        )
        interest_rate_preference = st.selectbox(
            "Interest Rate Preference",
            ["Fixed Rate", "Variable Rate", "Fixed-to-Variable", "No Preference"],
            key="ff_interest_rate"
        )
        urgency = st.selectbox(
            "Urgency Level",
            ["Urgent (< 2 weeks)", "High (2-4 weeks)", "Medium (1-2 months)", "Low (> 2 months)"],
            key="ff_urgency"
        )

with tab4:
    st.header("Financial Situation")
    
    # Pre-populate with data from previous steps
    employment_details = st.session_state.form_responses.get('employment_details', {})
    financial_details = st.session_state.form_responses.get('financial_details', {})
    
    # Income
    st.subheader("Income")
    col1, col2 = st.columns(2)
    
    with col1:
        employment_status = st.selectbox(
            "Employment Status",
            ["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed", "Other"],
            index=["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed", "Other"].index(employment_details.get('employment_status', "Employed Full-Time")) if employment_details.get('employment_status') else 0,
            key="ff_employment_status"
        )
        employer_name = st.text_input(
            "Employer/Business Name", 
            value=employment_details.get('employer_name', ''),
            key="ff_employer_name"
        )
        job_title = st.text_input(
            "Job Title/Position", 
            value=employment_details.get('job_title', ''),
            key="ff_job_title"
        )
        
    with col2:
        years_employed = st.number_input(
            "Years with Current Employer/Business", 
            min_value=0.0, 
            value=float(employment_details.get('years_employed', 0)),
            step=0.5, 
            key="ff_years_employed"
        )
        annual_income = st.number_input(
            "Annual Income ($)", 
            min_value=0, 
            value=int(employment_details.get('annual_income', 0)),
            step=5000, 
            key="ff_annual_income"
        )
        additional_income = st.number_input(
            "Additional Monthly Income ($)", 
            min_value=0, 
            value=int(employment_details.get('additional_income_amount', 0)),
            step=100, 
            key="ff_additional_income"
        )
    
    # Expenses and Debts
    st.subheader("Expenses and Debts")
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_expenses = st.number_input(
            "Monthly Living Expenses ($)", 
            min_value=0, 
            step=100, 
            key="ff_monthly_expenses"
        )
        existing_mortgage = st.number_input(
            "Existing Mortgage Payment ($)", 
            min_value=0, 
            step=100, 
            key="ff_existing_mortgage"
        )
        
    with col2:
        credit_card_debt = st.number_input(
            "Credit Card Debt ($)", 
            min_value=0, 
            step=100, 
            key="ff_credit_card_debt"
        )
        other_loans = st.number_input(
            "Other Loan Payments (monthly, $)", 
            min_value=0, 
            step=100, 
            key="ff_other_loans"
        )
    
    # Assets
    st.subheader("Assets")
    col1, col2 = st.columns(2)
    
    with col1:
        savings = st.number_input(
            "Savings ($)", 
            min_value=0, 
            step=1000, 
            key="ff_savings"
        )
        investments = st.number_input(
            "Investments ($)", 
            min_value=0, 
            step=1000, 
            key="ff_investments"
        )
        
    with col2:
        other_properties = st.number_input(
            "Value of Other Properties ($)", 
            min_value=0, 
            step=10000, 
            key="ff_other_properties"
        )
        other_assets = st.number_input(
            "Other Assets ($)", 
            min_value=0, 
            step=1000, 
            key="ff_other_assets"
        )

with tab5:
    st.header("Risk Profile")
    
    # Credit History
    st.subheader("Credit History")
    
    credit_score = st.selectbox(
        "Credit Score Range",
        ["Below 600", "600-650", "650-700", "700-750", "750+", "Unsure"],
        index=["Below 600", "600-650", "650-700", "700-750", "750+", "Unsure"].index(financial_details.get('credit_score', "Unsure")) if financial_details.get('credit_score') else 5,
        key="ff_credit_score"
    )
    
    bankruptcy = st.selectbox(
        "Bankruptcy History",
        ["No", "Yes - Discharged", "Yes - Not Discharged"],
        index=["No", "Yes - Discharged", "Yes - Not Discharged"].index(financial_details.get('bankruptcy', "No")) if financial_details.get('bankruptcy') else 0,
        key="ff_bankruptcy"
    )
    
    missed_payments = st.selectbox(
        "Missed Payments (last 12 months)",
        ["None", "1-2", "3-5", "More than 5"],
        key="ff_missed_payments"
    )
    
    # Risk Factors
    st.subheader("Additional Risk Factors")
    
    risk_factors = st.multiselect(
        "Select all that apply",
        [
            "Self-employed less than 2 years",
            "Income primarily from commissions/bonuses",
            "Previous foreclosure",
            "High debt-to-income ratio",
            "Non-standard property type",
            "Foreign national",
            "Limited credit history",
            "Recent job change",
            "Interest-only loan preference",
            "Large loan amount"
        ],
        key="ff_risk_factors"
    )
    
    # Client Preferences
    st.subheader("Client Preferences and Flexibility")
    
    rate_vs_fee = st.slider(
        "Rate vs. Fee Preference",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Lowest rate (higher fees), 5 = Lowest fees (higher rate)",
        key="ff_rate_vs_fee"
    )
    
    payment_flexibility = st.slider(
        "Payment Flexibility Importance",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Fixed payments, 5 = Maximum flexibility",
        key="ff_payment_flexibility"
    )
    
    early_repayment = st.slider(
        "Early Repayment Importance",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Not important, 5 = Very important",
        key="ff_early_repayment"
    )

# Additional Notes
st.header("Additional Notes")
additional_notes = st.text_area("Additional information or special circumstances", height=150, key="ff_additional_notes")

# Save and Continue Button
if st.button("Save and Complete Fact-Find"):
    # Save all fact-find data to session state
    st.session_state.fact_find_data['meeting_details'] = {
        'meeting_date': meeting_date.strftime("%Y-%m-%d") if meeting_date else None,
        'meeting_time': meeting_time.strftime("%H:%M") if meeting_time else None,
        'meeting_duration': meeting_duration,
        'meeting_type': meeting_type,
        'broker_name': broker_name,
        'meeting_notes': meeting_notes,
        'transcript_file': transcript_file.name if transcript_file else None
    }
    
    st.session_state.fact_find_data['client_profile'] = {
        'first_name': first_name,
        'last_name': last_name,
        'dob': dob.strftime("%Y-%m-%d") if dob else None,
        'marital_status': marital_status,
        'email': email,
        'phone': phone,
        'address': address,
        'years_at_address': years_at_address,
        'has_dependents': has_dependents,
        'num_dependents': num_dependents if 'num_dependents' in locals() else None,
        'dependent_ages': dependent_ages if 'dependent_ages' in locals() else None
    }
    
    st.session_state.fact_find_data['property_details'] = {
        'property_type': property_type,
        'property_value': property_value,
        'property_age': property_age,
        'property_use': property_use,
        'property_address': property_address,
        'property_condition': property_condition
    }
    
    st.session_state.fact_find_data['loan_requirements'] = {
        'loan_purpose': loan_purpose,
        'loan_amount': loan_amount,
        'down_payment': down_payment,
        'loan_term_preference': loan_term_preference,
        'interest_rate_preference': interest_rate_preference,
        'urgency': urgency
    }
    
    st.session_state.fact_find_data['financial_situation'] = {
        'employment_status': employment_status,
        'employer_name': employer_name,
        'job_title': job_title,
        'years_employed': years_employed,
        'annual_income': annual_income,
        'additional_income': additional_income,
        'monthly_expenses': monthly_expenses,
        'existing_mortgage': existing_mortgage,
        'credit_card_debt': credit_card_debt,
        'other_loans': other_loans,
        'savings': savings,
        'investments': investments,
        'other_properties': other_properties,
        'other_assets': other_assets
    }
    
    st.session_state.fact_find_data['risk_profile'] = {
        'credit_score': credit_score,
        'bankruptcy': bankruptcy,
        'missed_payments': missed_payments,
        'risk_factors': risk_factors,
        'rate_vs_fee': rate_vs_fee,
        'payment_flexibility': payment_flexibility,
        'early_repayment': early_repayment
    }
    
    st.session_state.fact_find_data['additional_notes'] = {
        'notes': additional_notes
    }
    
    # Generate output
    st.session_state.outputs = {
        'complete_data_set': True
    }
    
    st.success("Fact-find completed successfully! A complete data set has been generated.")
    
    # Display output
    st.subheader("Output Generated")
    st.markdown("✅ Complete client data set created")
    
    st.balloons()

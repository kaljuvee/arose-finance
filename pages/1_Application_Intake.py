import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Application Intake",
    page_icon="📝",
    layout="wide"
)

st.title("Step 1: Application Intake")
st.markdown("Collect borrower information and loan request details")

# Initialize session state for storing application data
if 'application_data' not in st.session_state:
    st.session_state.application_data = {
        'personal_info': {},
        'loan_info': {},
        'employment_info': {},
        'financial_info': {}
    }

# Create tabs for different sections of the application
tab1, tab2, tab3, tab4 = st.tabs(["Personal Information", "Loan Details", "Employment Information", "Financial Information"])

with tab1:
    st.header("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name", key="first_name")
        last_name = st.text_input("Last Name", key="last_name")
        dob = st.date_input("Date of Birth", min_value=date(1900, 1, 1), max_value=date.today(), key="dob")
        ssn = st.text_input("Social Security Number (XXX-XX-XXXX)", key="ssn")
    
    with col2:
        email = st.text_input("Email Address", key="email")
        phone = st.text_input("Phone Number", key="phone")
        address = st.text_area("Current Address", key="address")
        years_at_address = st.number_input("Years at Current Address", min_value=0.0, step=0.5, key="years_at_address")

with tab2:
    st.header("Loan Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation", "Other"],
            key="loan_purpose"
        )
        loan_amount = st.number_input("Requested Loan Amount ($)", min_value=1000, step=1000, key="loan_amount")
        
    with col2:
        loan_term = st.selectbox(
            "Loan Term (Years)",
            [5, 10, 15, 20, 30],
            key="loan_term"
        )
        if loan_purpose == "Other":
            other_purpose = st.text_input("Please specify purpose", key="other_purpose")

with tab3:
    st.header("Employment Information")
    
    employment_status = st.selectbox(
        "Employment Status",
        ["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed"],
        key="employment_status"
    )
    
    if employment_status in ["Employed Full-Time", "Employed Part-Time", "Self-Employed"]:
        col1, col2 = st.columns(2)
        
        with col1:
            employer_name = st.text_input("Employer Name", key="employer_name")
            job_title = st.text_input("Job Title", key="job_title")
            
        with col2:
            years_employed = st.number_input("Years with Current Employer", min_value=0.0, step=0.5, key="years_employed")
            monthly_income = st.number_input("Gross Monthly Income ($)", min_value=0, step=100, key="monthly_income")

with tab4:
    st.header("Financial Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        bank_name = st.text_input("Primary Bank Name", key="bank_name")
        account_type = st.selectbox(
            "Account Type",
            ["Checking", "Savings", "Both"],
            key="account_type"
        )
        
    with col2:
        monthly_expenses = st.number_input("Total Monthly Expenses ($)", min_value=0, step=100, key="monthly_expenses")
        existing_debts = st.number_input("Total Existing Debt ($)", min_value=0, step=1000, key="existing_debts")

# Save application data
if st.button("Save and Continue"):
    # Update session state with form data
    # Personal Info
    st.session_state.application_data['personal_info'] = {
        'first_name': first_name,
        'last_name': last_name,
        'dob': dob.strftime("%Y-%m-%d") if dob else None,
        'ssn': ssn,
        'email': email,
        'phone': phone,
        'address': address,
        'years_at_address': years_at_address
    }
    
    # Loan Info
    st.session_state.application_data['loan_info'] = {
        'loan_purpose': loan_purpose,
        'loan_amount': loan_amount,
        'loan_term': loan_term
    }
    
    # Employment Info
    st.session_state.application_data['employment_info'] = {
        'employment_status': employment_status,
        'employer_name': employer_name if 'employer_name' in locals() else None,
        'job_title': job_title if 'job_title' in locals() else None,
        'years_employed': years_employed if 'years_employed' in locals() else None,
        'monthly_income': monthly_income if 'monthly_income' in locals() else None
    }
    
    # Financial Info
    st.session_state.application_data['financial_info'] = {
        'bank_name': bank_name,
        'account_type': account_type,
        'monthly_expenses': monthly_expenses,
        'existing_debts': existing_debts
    }
    
    st.success("Application information saved successfully! Please proceed to the next step.")
    st.balloons() 
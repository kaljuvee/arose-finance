import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Broker Verification",
    page_icon="✅",
    layout="wide"
)

st.title("Step 4: Broker Verification")
st.markdown("Verify and approve the transcoded client profile")

# Check if previous steps are completed
if 'fact_find_data' not in st.session_state:
    st.warning("Please complete Step 3: Fact-Find Completion first.")
    st.stop()

# Initialize session state for broker verification
if 'broker_verification' not in st.session_state:
    st.session_state.broker_verification = {
        'verified': False,
        'edits_made': {},
        'approval_timestamp': None,
        'broker_notes': ''
    }

# Create tabs for different sections of verification
tab1, tab2, tab3, tab4 = st.tabs([
    "Client Profile", 
    "Property & Loan Details", 
    "Financial Profile", 
    "Approval"
])

with tab1:
    st.header("Client Profile Verification")
    st.info("Review the transcoded client profile information and make corrections if needed.")
    
    # Get client profile data from fact-find
    client_profile = st.session_state.fact_find_data.get('client_profile', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Personal Information")
        
        # Display and allow editing of personal information
        first_name = st.text_input(
            "First Name", 
            value=client_profile.get('first_name', ''),
            key="verify_first_name"
        )
        
        last_name = st.text_input(
            "Last Name", 
            value=client_profile.get('last_name', ''),
            key="verify_last_name"
        )
        
        dob = st.date_input(
            "Date of Birth", 
            value=pd.to_datetime(client_profile.get('dob', '1980-01-01')) if client_profile.get('dob') else pd.to_datetime('1980-01-01'),
            key="verify_dob"
        )
        
        marital_status = st.selectbox(
            "Marital Status",
            ["Single", "Married", "Civil Partnership", "Divorced", "Widowed", "Separated"],
            index=["Single", "Married", "Civil Partnership", "Divorced", "Widowed", "Separated"].index(client_profile.get('marital_status', "Single")) if client_profile.get('marital_status') else 0,
            key="verify_marital_status"
        )
    
    with col2:
        st.subheader("Contact Information")
        
        email = st.text_input(
            "Email Address", 
            value=client_profile.get('email', ''),
            key="verify_email"
        )
        
        phone = st.text_input(
            "Phone Number", 
            value=client_profile.get('phone', ''),
            key="verify_phone"
        )
        
        address = st.text_area(
            "Current Address", 
            value=client_profile.get('address', ''),
            key="verify_address"
        )
        
        years_at_address = st.number_input(
            "Years at Current Address", 
            min_value=0.0, 
            value=float(client_profile.get('years_at_address', 0)),
            step=0.5, 
            key="verify_years_at_address"
        )
    
    # Dependents information
    st.subheader("Dependents")
    has_dependents = st.checkbox(
        "Client has dependents", 
        value=client_profile.get('has_dependents', False),
        key="verify_has_dependents"
    )
    
    if has_dependents:
        col1, col2 = st.columns(2)
        
        with col1:
            num_dependents = st.number_input(
                "Number of Dependents", 
                min_value=1, 
                max_value=10, 
                value=int(client_profile.get('num_dependents', 1)),
                step=1, 
                key="verify_num_dependents"
            )
        
        with col2:
            dependent_ages = st.text_input(
                "Ages of Dependents (comma separated)", 
                value=client_profile.get('dependent_ages', ''),
                key="verify_dependent_ages"
            )

with tab2:
    st.header("Property & Loan Details Verification")
    
    # Get property and loan details from fact-find
    property_details = st.session_state.fact_find_data.get('property_details', {})
    loan_requirements = st.session_state.fact_find_data.get('loan_requirements', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Property Information")
        
        property_type = st.selectbox(
            "Property Type",
            ["Single Family Home", "Multi-Family Home", "Condominium", "Townhouse", "Commercial Property", "Land"],
            index=["Single Family Home", "Multi-Family Home", "Condominium", "Townhouse", "Commercial Property", "Land"].index(property_details.get('property_type', "Single Family Home")) if property_details.get('property_type') else 0,
            key="verify_property_type"
        )
        
        property_value = st.number_input(
            "Estimated Property Value ($)", 
            min_value=0, 
            value=int(property_details.get('property_value', 0)),
            step=10000, 
            key="verify_property_value"
        )
        
        property_age = st.number_input(
            "Property Age (years)", 
            min_value=0, 
            value=int(property_details.get('property_age', 0)),
            step=1, 
            key="verify_property_age"
        )
        
        property_condition = st.selectbox(
            "Property Condition",
            ["Excellent", "Good", "Fair", "Poor", "Needs Renovation"],
            index=["Excellent", "Good", "Fair", "Poor", "Needs Renovation"].index(property_details.get('property_condition', "Good")) if property_details.get('property_condition') else 1,
            key="verify_property_condition"
        )
    
    with col2:
        st.subheader("Loan Requirements")
        
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation", "Business", "Other"],
            index=["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation", "Business", "Other"].index(loan_requirements.get('loan_purpose', "Home Purchase")) if loan_requirements.get('loan_purpose') else 0,
            key="verify_loan_purpose"
        )
        
        loan_amount = st.number_input(
            "Requested Loan Amount ($)", 
            min_value=0, 
            value=int(loan_requirements.get('loan_amount', 0)),
            step=10000, 
            key="verify_loan_amount"
        )
        
        down_payment = st.number_input(
            "Down Payment Amount ($)", 
            min_value=0, 
            value=int(loan_requirements.get('down_payment', 0)),
            step=5000, 
            key="verify_down_payment"
        )
        
        loan_term_preference = st.selectbox(
            "Preferred Loan Term",
            ["15 years", "20 years", "25 years", "30 years", "Other"],
            index=["15 years", "20 years", "25 years", "30 years", "Other"].index(loan_requirements.get('loan_term_preference', "30 years")) if loan_requirements.get('loan_term_preference') else 3,
            key="verify_loan_term"
        )
    
    # Property address
    st.subheader("Property Location")
    property_address = st.text_area(
        "Property Address", 
        value=property_details.get('property_address', ''),
        key="verify_property_address"
    )
    
    property_use = st.selectbox(
        "Property Use",
        ["Primary Residence", "Secondary/Vacation Home", "Investment Property", "Business"],
        index=["Primary Residence", "Secondary/Vacation Home", "Investment Property", "Business"].index(property_details.get('property_use', "Primary Residence")) if property_details.get('property_use') else 0,
        key="verify_property_use"
    )

with tab3:
    st.header("Financial Profile Verification")
    
    # Get financial data from fact-find
    financial_situation = st.session_state.fact_find_data.get('financial_situation', {})
    risk_profile = st.session_state.fact_find_data.get('risk_profile', {})
    
    # Income
    st.subheader("Income Verification")
    col1, col2 = st.columns(2)
    
    with col1:
        employment_status = st.selectbox(
            "Employment Status",
            ["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed", "Other"],
            index=["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed", "Other"].index(financial_situation.get('employment_status', "Employed Full-Time")) if financial_situation.get('employment_status') else 0,
            key="verify_employment_status"
        )
        
        employer_name = st.text_input(
            "Employer/Business Name", 
            value=financial_situation.get('employer_name', ''),
            key="verify_employer_name"
        )
        
        years_employed = st.number_input(
            "Years with Current Employer/Business", 
            min_value=0.0, 
            value=float(financial_situation.get('years_employed', 0)),
            step=0.5, 
            key="verify_years_employed"
        )
    
    with col2:
        annual_income = st.number_input(
            "Annual Income ($)", 
            min_value=0, 
            value=int(financial_situation.get('annual_income', 0)),
            step=5000, 
            key="verify_annual_income"
        )
        
        additional_income = st.number_input(
            "Additional Monthly Income ($)", 
            min_value=0, 
            value=int(financial_situation.get('additional_income', 0)),
            step=100, 
            key="verify_additional_income"
        )
        
        total_monthly_income = (annual_income / 12) + additional_income
        st.metric("Total Monthly Income", f"${total_monthly_income:,.2f}")
    
    # Expenses and Debts
    st.subheader("Expenses and Debts Verification")
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_expenses = st.number_input(
            "Monthly Living Expenses ($)", 
            min_value=0, 
            value=int(financial_situation.get('monthly_expenses', 0)),
            step=100, 
            key="verify_monthly_expenses"
        )
        
        existing_mortgage = st.number_input(
            "Existing Mortgage Payment ($)", 
            min_value=0, 
            value=int(financial_situation.get('existing_mortgage', 0)),
            step=100, 
            key="verify_existing_mortgage"
        )
    
    with col2:
        credit_card_debt = st.number_input(
            "Credit Card Debt ($)", 
            min_value=0, 
            value=int(financial_situation.get('credit_card_debt', 0)),
            step=100, 
            key="verify_credit_card_debt"
        )
        
        other_loans = st.number_input(
            "Other Loan Payments (monthly, $)", 
            min_value=0, 
            value=int(financial_situation.get('other_loans', 0)),
            step=100, 
            key="verify_other_loans"
        )
    
    # Credit Profile
    st.subheader("Credit Profile Verification")
    col1, col2 = st.columns(2)
    
    with col1:
        credit_score = st.selectbox(
            "Credit Score Range",
            ["Below 600", "600-650", "650-700", "700-750", "750+", "Unsure"],
            index=["Below 600", "600-650", "650-700", "700-750", "750+", "Unsure"].index(risk_profile.get('credit_score', "Unsure")) if risk_profile.get('credit_score') else 5,
            key="verify_credit_score"
        )
    
    with col2:
        bankruptcy = st.selectbox(
            "Bankruptcy History",
            ["No", "Yes - Discharged", "Yes - Not Discharged"],
            index=["No", "Yes - Discharged", "Yes - Not Discharged"].index(risk_profile.get('bankruptcy', "No")) if risk_profile.get('bankruptcy') else 0,
            key="verify_bankruptcy"
        )
    
    # Risk Factors
    st.subheader("Risk Factors Verification")
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
        default=risk_profile.get('risk_factors', []),
        key="verify_risk_factors"
    )

with tab4:
    st.header("Profile Approval")
    
    # Display summary of key information
    st.subheader("Client Profile Summary")
    
    summary_col1, summary_col2 = st.columns(2)
    
    with summary_col1:
        st.write(f"**Client:** {first_name} {last_name}")
        st.write(f"**Loan Purpose:** {loan_purpose}")
        st.write(f"**Loan Amount:** ${loan_amount:,}")
        st.write(f"**Property Type:** {property_type}")
        st.write(f"**Property Value:** ${property_value:,}")
    
    with summary_col2:
        st.write(f"**Employment:** {employment_status}")
        st.write(f"**Annual Income:** ${annual_income:,}")
        st.write(f"**Credit Score:** {credit_score}")
        st.write(f"**Property Use:** {property_use}")
        st.write(f"**LTV Ratio:** {(loan_amount / property_value * 100) if property_value > 0 else 0:.1f}%")
    
    # Broker notes
    st.subheader("Broker Notes")
    broker_notes = st.text_area(
        "Add any additional notes or observations", 
        value=st.session_state.broker_verification.get('broker_notes', ''),
        height=150,
        key="broker_notes"
    )
    
    # Track edits made
    edits_made = {}
    
    # Compare original client profile with verified values
    if client_profile.get('first_name') != first_name:
        edits_made['first_name'] = {'original': client_profile.get('first_name'), 'new': first_name}
    
    if client_profile.get('last_name') != last_name:
        edits_made['last_name'] = {'original': client_profile.get('last_name'), 'new': last_name}
    
    # Display edits if any were made
    if edits_made:
        st.subheader("Edits Made")
        st.info(f"{len(edits_made)} changes were made to the original profile.")
        
        edits_df = pd.DataFrame([
            {
                'Field': field,
                'Original Value': edits_made[field]['original'],
                'New Value': edits_made[field]['new']
            }
            for field in edits_made
        ])
        
        st.dataframe(edits_df, use_container_width=True)
    else:
        st.success("No edits were made to the original profile.")
    
    # Approval button
    if st.button("Approve Client Profile"):
        # Save verification data
        st.session_state.broker_verification = {
            'verified': True,
            'edits_made': edits_made,
            'approval_timestamp': pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            'broker_notes': broker_notes
        }
        
        # Save verified client profile
        st.session_state.verified_profile = {
            'client_profile': {
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
            },
            'property_details': {
                'property_type': property_type,
                'property_value': property_value,
                'property_age': property_age,
                'property_condition': property_condition,
                'property_address': property_address,
                'property_use': property_use
            },
            'loan_requirements': {
                'loan_purpose': loan_purpose,
                'loan_amount': loan_amount,
                'down_payment': down_payment,
                'loan_term_preference': loan_term_preference
            },
            'financial_profile': {
                'employment_status': employment_status,
                'employer_name': employer_name,
                'years_employed': years_employed,
                'annual_income': annual_income,
                'additional_income': additional_income,
                'monthly_expenses': monthly_expenses,
                'existing_mortgage': existing_mortgage,
                'credit_card_debt': credit_card_debt,
                'other_loans': other_loans,
                'credit_score': credit_score,
                'bankruptcy': bankruptcy,
                'risk_factors': risk_factors
            }
        }
        
        st.success("Client profile has been verified and approved!")
        st.balloons()
        
        # Display output
        st.subheader("Output Generated")
        st.markdown("✅ Manual edit/verification from broker")
        st.markdown("✅ Approval of client profile")
        
        # If edits were made, show machine learning feedback
        if edits_made:
            st.info("The transcoding logic has been educated on the corrections made and will improve future interpretations.")
            
            # Display a few examples of how the system learned
            st.subheader("Machine Learning Feedback")
            for field in list(edits_made.keys())[:3]:  # Show up to 3 examples
                st.write(f"✓ Learned that '{edits_made[field]['original']}' should be interpreted as '{edits_made[field]['new']}' for field '{field}'") 
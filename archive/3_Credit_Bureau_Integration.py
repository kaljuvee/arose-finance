import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Credit Bureau Integration",
    page_icon="📊",
    layout="wide"
)

st.title("Step 3: Credit Bureau Integration")
st.markdown("Retrieve and analyze credit reports")

# Initialize session state for credit data
if 'credit_data' not in st.session_state:
    st.session_state.credit_data = {
        'credit_score': None,
        'report_date': None,
        'credit_history': None,
        'accounts': None,
        'inquiries': None,
        'public_records': None
    }

# Function to generate mock credit data
def generate_credit_data(ssn=None):
    # This is a placeholder function that would be replaced with actual API integration
    
    # Generate a random credit score between 300 and 850
    credit_score = np.random.randint(300, 851)
    
    # Generate a report date (today)
    report_date = datetime.now().strftime("%Y-%m-%d")
    
    # Generate credit history length (1-30 years)
    credit_history = np.random.randint(1, 31)
    
    # Generate accounts data
    num_accounts = np.random.randint(3, 15)
    accounts = []
    
    account_types = ["Credit Card", "Auto Loan", "Mortgage", "Personal Loan", "Student Loan"]
    statuses = ["Current", "Current", "Current", "Current", "Late 30", "Late 60", "Late 90+", "Closed"]
    
    for i in range(num_accounts):
        account = {
            "account_type": np.random.choice(account_types),
            "opened_date": (datetime.now() - timedelta(days=np.random.randint(30, 3650))).strftime("%Y-%m-%d"),
            "balance": round(np.random.uniform(0, 50000), 2),
            "credit_limit": round(np.random.uniform(1000, 100000), 2),
            "status": np.random.choice(statuses, p=[0.7, 0.1, 0.05, 0.05, 0.03, 0.02, 0.01, 0.04])
        }
        accounts.append(account)
    
    # Generate inquiries
    num_inquiries = np.random.randint(0, 6)
    inquiries = []
    
    inquiry_types = ["Auto Loan", "Credit Card", "Mortgage", "Personal Loan"]
    
    for i in range(num_inquiries):
        inquiry = {
            "inquiry_date": (datetime.now() - timedelta(days=np.random.randint(1, 730))).strftime("%Y-%m-%d"),
            "inquiry_type": np.random.choice(inquiry_types)
        }
        inquiries.append(inquiry)
    
    # Generate public records
    has_public_records = np.random.choice([True, False], p=[0.05, 0.95])
    public_records = []
    
    if has_public_records:
        num_records = np.random.randint(1, 3)
        record_types = ["Bankruptcy", "Tax Lien", "Civil Judgment"]
        
        for i in range(num_records):
            record = {
                "record_type": np.random.choice(record_types),
                "filing_date": (datetime.now() - timedelta(days=np.random.randint(30, 2555))).strftime("%Y-%m-%d"),
                "status": np.random.choice(["Satisfied", "Unsatisfied"])
            }
            public_records.append(record)
    
    return {
        'credit_score': credit_score,
        'report_date': report_date,
        'credit_history': credit_history,
        'accounts': accounts,
        'inquiries': inquiries,
        'public_records': public_records
    }

# Credit Bureau Selection
st.header("Credit Bureau Selection")

bureau_col1, bureau_col2 = st.columns(2)

with bureau_col1:
    selected_bureau = st.selectbox(
        "Select Credit Bureau",
        ["Experian", "TransUnion", "Equifax"],
        key="selected_bureau"
    )

with bureau_col2:
    report_type = st.selectbox(
        "Report Type",
        ["Standard", "Comprehensive", "Mortgage"],
        key="report_type"
    )

# Borrower Information Confirmation
st.header("Borrower Information Confirmation")

# Check if application data exists in session state
if 'application_data' in st.session_state and st.session_state.application_data['personal_info']:
    personal_info = st.session_state.application_data['personal_info']
    
    confirm_col1, confirm_col2 = st.columns(2)
    
    with confirm_col1:
        st.text_input("First Name", value=personal_info.get('first_name', ''), key="confirm_first_name")
        st.text_input("Last Name", value=personal_info.get('last_name', ''), key="confirm_last_name")
    
    with confirm_col2:
        st.text_input("Social Security Number", value=personal_info.get('ssn', ''), key="confirm_ssn")
        st.date_input("Date of Birth", value=datetime.strptime(personal_info.get('dob', datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d") if personal_info.get('dob') else datetime.now(), key="confirm_dob")
else:
    st.warning("No application data found. Please complete the Application Intake step first.")
    
    confirm_col1, confirm_col2 = st.columns(2)
    
    with confirm_col1:
        st.text_input("First Name", key="confirm_first_name")
        st.text_input("Last Name", key="confirm_last_name")
    
    with confirm_col2:
        st.text_input("Social Security Number", key="confirm_ssn")
        st.date_input("Date of Birth", key="confirm_dob")

# Pull Credit Report Button
if st.button("Pull Credit Report"):
    with st.spinner(f"Retrieving credit report from {selected_bureau}..."):
        # Simulate API call delay
        time.sleep(3)
        
        # Generate mock credit data
        st.session_state.credit_data = generate_credit_data(st.session_state.get("confirm_ssn", ""))
        
        st.success(f"Credit report successfully retrieved from {selected_bureau}!")

# Display Credit Report if available
if st.session_state.credit_data['credit_score'] is not None:
    st.header("Credit Report Summary")
    
    # Credit Score Display
    score_col1, score_col2, score_col3 = st.columns([2, 1, 1])
    
    with score_col1:
        credit_score = st.session_state.credit_data['credit_score']
        
        # Determine score category and color
        if credit_score >= 750:
            category = "Excellent"
            color = "green"
        elif credit_score >= 700:
            category = "Good"
            color = "lightgreen"
        elif credit_score >= 650:
            category = "Fair"
            color = "yellow"
        elif credit_score >= 600:
            category = "Poor"
            color = "orange"
        else:
            category = "Very Poor"
            color = "red"
        
        # Create a gauge chart for credit score using Plotly
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=credit_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Credit Score: {category}", 'font': {'size': 24}},
            gauge={
                'axis': {'range': [300, 850], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [300, 600], 'color': 'red'},
                    {'range': [600, 650], 'color': 'orange'},
                    {'range': [650, 700], 'color': 'yellow'},
                    {'range': [700, 750], 'color': 'lightgreen'},
                    {'range': [750, 850], 'color': 'green'}
                ],
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with score_col2:
        st.metric("Report Date", st.session_state.credit_data['report_date'])
        st.metric("Credit History Length", f"{st.session_state.credit_data['credit_history']} years")
    
    with score_col3:
        st.metric("Total Accounts", len(st.session_state.credit_data['accounts']))
        st.metric("Recent Inquiries", len(st.session_state.credit_data['inquiries']))
    
    # Accounts Summary
    st.subheader("Accounts Summary")
    
    if st.session_state.credit_data['accounts']:
        accounts_df = pd.DataFrame(st.session_state.credit_data['accounts'])
        st.dataframe(accounts_df, use_container_width=True)
    else:
        st.info("No account information available.")
    
    # Inquiries
    st.subheader("Recent Inquiries")
    
    if st.session_state.credit_data['inquiries']:
        inquiries_df = pd.DataFrame(st.session_state.credit_data['inquiries'])
        st.dataframe(inquiries_df, use_container_width=True)
    else:
        st.info("No recent inquiries found.")
    
    # Public Records
    st.subheader("Public Records")
    
    if st.session_state.credit_data['public_records']:
        records_df = pd.DataFrame(st.session_state.credit_data['public_records'])
        st.dataframe(records_df, use_container_width=True)
    else:
        st.success("No public records found.")
    
    # Save and Continue Button
    if st.button("Save and Continue to Financial Analysis"):
        st.session_state.credit_bureau_complete = True
        st.success("Credit report data saved successfully! Please proceed to the Financial Analysis step.")
        st.balloons()
else:
    st.info("Please pull a credit report to view the summary.") 
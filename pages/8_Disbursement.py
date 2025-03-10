import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import time
import random

st.set_page_config(
    page_title="Disbursement",
    page_icon="💸",
    layout="wide"
)

st.title("Step 8: Disbursement")
st.markdown("Process loan funding and distribution")

# Initialize session state for disbursement
if 'disbursement' not in st.session_state:
    st.session_state.disbursement = {
        'disbursement_status': None,
        'disbursement_date': None,
        'disbursement_method': None,
        'disbursement_amount': None,
        'recipient_info': {},
        'transaction_id': None
    }

# Check if we have approval process data
has_approval = 'approval_process' in st.session_state and st.session_state.approval_process.get('approval_status')

# Check if we have loan structure data
has_loan_structure = 'loan_structure' in st.session_state and st.session_state.loan_structure.get('loan_type')

if not has_approval or not has_loan_structure:
    st.warning("Complete previous steps before proceeding with disbursement.")
    if not has_approval:
        st.error("Missing approval data. Please complete the Approval Process step.")
    if not has_loan_structure:
        st.error("Missing loan structure data. Please complete the Loan Structuring step.")
else:
    # Get data from session state
    approval_process = st.session_state.approval_process
    loan_structure = st.session_state.loan_structure
    application_data = st.session_state.application_data if 'application_data' in st.session_state else None
    
    # Check approval status
    approval_status = approval_process.get('approval_status', 'Unknown')
    
    if approval_status not in ["Approved", "Approved with Conditions"]:
        st.error("❌ Loan application is not approved for disbursement.")
        st.info("Please return to the Approval Process step to review the application status.")
        st.stop()
    
    # Display approval information
    st.header("Approval Information")
    
    approval_col1, approval_col2 = st.columns(2)
    
    with approval_col1:
        st.subheader("Approval Status")
        st.success(f"✅ {approval_status}")
        st.write(f"**Approval Date:** {approval_process.get('approval_date', 'Not specified')}")
        st.write(f"**Approved By:** {approval_process.get('approved_by', 'Not specified')}")
        st.write(f"**Approval ID:** {approval_process.get('approval_id', 'Not specified')}")
    
    with approval_col2:
        st.subheader("Loan Details")
        st.write(f"**Loan Type:** {loan_structure.get('loan_type', 'Not specified')}")
        st.write(f"**Loan Amount:** ${loan_structure.get('loan_amount', application_data['loan_info'].get('loan_amount', 0)):,.2f}")
        st.write(f"**Interest Rate:** {loan_structure.get('interest_rate', 0):.3f}%")
        st.write(f"**Loan Term:** {loan_structure.get('loan_term', 0)} years")
    
    # Display any approval conditions
    if approval_status == "Approved with Conditions" and approval_process.get('conditions'):
        st.subheader("Approval Conditions")
        
        # Create a dataframe for conditions
        conditions_data = {
            "Condition": approval_process['conditions'],
            "Status": ["Pending Verification" for _ in approval_process['conditions']]
        }
        
        conditions_df = pd.DataFrame(conditions_data)
        
        # Allow updating condition status
        for i, condition in enumerate(conditions_df["Condition"]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{i+1}. {condition}**")
            with col2:
                status = st.selectbox(
                    "Status",
                    ["Pending Verification", "Verified", "Waived"],
                    index=0,
                    key=f"condition_status_{i}"
                )
                conditions_df.at[i, "Status"] = status
        
        # Check if all conditions are satisfied
        all_conditions_met = all(status in ["Verified", "Waived"] for status in conditions_df["Status"])
        
        if not all_conditions_met:
            st.warning("⚠️ All conditions must be verified or waived before proceeding with disbursement.")
        else:
            st.success("✅ All conditions have been satisfied.")
    
    # Closing Information
    st.header("Closing Information")
    
    # Check if closing is complete
    if 'closing_complete' not in st.session_state:
        st.session_state.closing_complete = False
    
    if not st.session_state.closing_complete:
        closing_col1, closing_col2 = st.columns(2)
        
        with closing_col1:
            st.subheader("Closing Details")
            
            closing_date = st.date_input(
                "Closing Date",
                value=datetime.now(),
                key="closing_date"
            )
            
            closing_location = st.selectbox(
                "Closing Location",
                ["Title Company Office", "Lender's Office", "Attorney's Office", "Remote/Virtual Closing"],
                index=0,
                key="closing_location"
            )
            
            closing_agent = st.text_input(
                "Closing Agent/Attorney",
                value="ABC Title Company",
                key="closing_agent"
            )
        
        with closing_col2:
            st.subheader("Closing Checklist")
            
            # Create a checklist of required closing items
            closing_items = [
                "Loan documents signed",
                "Closing disclosure acknowledged",
                "Identification verified",
                "Funds received for closing costs",
                "Title insurance in place",
                "Homeowner's insurance verified",
                "Property taxes current"
            ]
            
            # Allow checking off items
            all_items_checked = True
            for item in closing_items:
                checked = st.checkbox(item, value=False, key=f"closing_{item.replace(' ', '_').lower()}")
                if not checked:
                    all_items_checked = False
        
        # Complete closing
        if st.button("Complete Closing Process"):
            if all_items_checked:
                with st.spinner("Processing closing documents..."):
                    # Simulate processing delay
                    time.sleep(2)
                    
                    st.session_state.closing_complete = True
                    st.success("✅ Closing process completed successfully!")
            else:
                st.error("❌ All closing checklist items must be completed before proceeding.")
    else:
        st.success("✅ Closing process has been completed.")
    
    # Disbursement Process
    st.header("Disbursement Process")
    
    # Check if disbursement is already complete
    if st.session_state.disbursement.get('disbursement_status') == "Complete":
        st.success(f"✅ Loan funds disbursed on {st.session_state.disbursement['disbursement_date']}")
        st.write(f"**Disbursement Method:** {st.session_state.disbursement['disbursement_method']}")
        st.write(f"**Disbursement Amount:** ${st.session_state.disbursement['disbursement_amount']:,.2f}")
        st.write(f"**Transaction ID:** {st.session_state.disbursement['transaction_id']}")
        
        # Display recipient information
        recipient_info = st.session_state.disbursement['recipient_info']
        st.subheader("Recipient Information")
        
        if recipient_info:
            for key, value in recipient_info.items():
                st.write(f"**{key}:** {value}")
        
        # Option to view disbursement confirmation
        if st.button("View Disbursement Confirmation"):
            with st.spinner("Generating confirmation..."):
                # Simulate document generation
                time.sleep(2)
                
                st.success("Disbursement confirmation generated successfully!")
                st.download_button(
                    label="Download Disbursement Confirmation",
                    data="This is a placeholder for the disbursement confirmation content.",
                    file_name="disbursement_confirmation.pdf",
                    mime="application/pdf"
                )
    else:
        # Check if closing is complete
        if not st.session_state.closing_complete:
            st.warning("⚠️ Closing process must be completed before disbursement.")
        elif approval_status == "Approved with Conditions" and not all_conditions_met:
            st.warning("⚠️ All approval conditions must be satisfied before disbursement.")
        else:
            # Disbursement form
            disbursement_col1, disbursement_col2 = st.columns(2)
            
            with disbursement_col1:
                st.subheader("Disbursement Details")
                
                disbursement_date = st.date_input(
                    "Disbursement Date",
                    value=datetime.now(),
                    key="disbursement_date"
                )
                
                disbursement_method = st.selectbox(
                    "Disbursement Method",
                    ["Wire Transfer", "ACH Transfer", "Cashier's Check", "Escrow Disbursement"],
                    index=0,
                    key="disbursement_method"
                )
                
                # Get loan amount
                loan_amount = loan_structure.get('loan_amount', application_data['loan_info'].get('loan_amount', 0))
                
                # Calculate net disbursement (loan amount minus closing costs)
                total_fees = loan_structure.get('total_fees', 0)
                net_disbursement = loan_amount - total_fees
                
                disbursement_amount = st.number_input(
                    "Disbursement Amount ($)",
                    min_value=0.0,
                    max_value=float(loan_amount * 1.1),  # Allow slight flexibility
                    value=float(net_disbursement),
                    step=100.0,
                    key="disbursement_amount"
                )
            
            with disbursement_col2:
                st.subheader("Recipient Information")
                
                if disbursement_method in ["Wire Transfer", "ACH Transfer"]:
                    recipient_name = st.text_input(
                        "Recipient Name",
                        value="",
                        key="recipient_name"
                    )
                    
                    bank_name = st.text_input(
                        "Bank Name",
                        value="",
                        key="bank_name"
                    )
                    
                    account_type = st.selectbox(
                        "Account Type",
                        ["Checking", "Savings"],
                        index=0,
                        key="account_type"
                    )
                    
                    routing_number = st.text_input(
                        "Routing Number",
                        value="",
                        key="routing_number"
                    )
                    
                    account_number = st.text_input(
                        "Account Number",
                        value="",
                        key="account_number",
                        type="password"
                    )
                elif disbursement_method == "Cashier's Check":
                    payee_name = st.text_input(
                        "Payee Name",
                        value="",
                        key="payee_name"
                    )
                    
                    mailing_address = st.text_area(
                        "Mailing Address",
                        value="",
                        key="mailing_address"
                    )
                else:  # Escrow Disbursement
                    escrow_company = st.text_input(
                        "Escrow/Title Company",
                        value="",
                        key="escrow_company"
                    )
                    
                    escrow_officer = st.text_input(
                        "Escrow Officer",
                        value="",
                        key="escrow_officer"
                    )
                    
                    escrow_number = st.text_input(
                        "Escrow Number",
                        value="",
                        key="escrow_number"
                    )
            
            # Process disbursement
            if st.button("Process Disbursement"):
                # Validate form based on disbursement method
                form_valid = True
                error_message = ""
                
                if disbursement_method in ["Wire Transfer", "ACH Transfer"]:
                    if not recipient_name or not bank_name or not routing_number or not account_number:
                        form_valid = False
                        error_message = "Please fill in all banking information fields."
                elif disbursement_method == "Cashier's Check":
                    if not payee_name or not mailing_address:
                        form_valid = False
                        error_message = "Please fill in payee name and mailing address."
                else:  # Escrow Disbursement
                    if not escrow_company or not escrow_number:
                        form_valid = False
                        error_message = "Please fill in escrow company and escrow number."
                
                if form_valid:
                    with st.spinner("Processing disbursement..."):
                        # Simulate processing delay
                        time.sleep(3)
                        
                        # Collect recipient information based on disbursement method
                        recipient_info = {}
                        
                        if disbursement_method in ["Wire Transfer", "ACH Transfer"]:
                            recipient_info = {
                                "Recipient Name": recipient_name,
                                "Bank Name": bank_name,
                                "Account Type": account_type,
                                "Routing Number": routing_number,
                                "Account Number": "****" + account_number[-4:] if account_number else ""
                            }
                        elif disbursement_method == "Cashier's Check":
                            recipient_info = {
                                "Payee Name": payee_name,
                                "Mailing Address": mailing_address
                            }
                        else:  # Escrow Disbursement
                            recipient_info = {
                                "Escrow Company": escrow_company,
                                "Escrow Officer": escrow_officer,
                                "Escrow Number": escrow_number
                            }
                        
                        # Generate transaction ID
                        transaction_id = f"TRX-{random.randint(100000, 999999)}"
                        
                        # Update session state with disbursement data
                        st.session_state.disbursement = {
                            'disbursement_status': "Complete",
                            'disbursement_date': disbursement_date.strftime("%Y-%m-%d"),
                            'disbursement_method': disbursement_method,
                            'disbursement_amount': disbursement_amount,
                            'recipient_info': recipient_info,
                            'transaction_id': transaction_id
                        }
                        
                        st.success(f"✅ Disbursement processed successfully! Transaction ID: {transaction_id}")
                        st.balloons()
                        
                        # Offer to download confirmation
                        st.download_button(
                            label="Download Disbursement Confirmation",
                            data="This is a placeholder for the disbursement confirmation content.",
                            file_name="disbursement_confirmation.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.error(f"❌ {error_message}")
    
    # Post-Disbursement Information
    st.header("Post-Disbursement Information")
    
    post_col1, post_col2 = st.columns(2)
    
    with post_col1:
        st.subheader("First Payment Information")
        
        # Calculate first payment date (typically first day of month after 30+ days)
        today = datetime.now()
        if today.day < 15:
            # If early in month, first payment is first of next month
            first_payment_date = datetime(today.year, today.month + 1 if today.month < 12 else 1, 1)
            if today.month == 12:
                first_payment_date = first_payment_date.replace(year=today.year + 1)
        else:
            # If late in month, first payment is first of month after next
            first_payment_date = datetime(today.year, today.month + 2 if today.month < 11 else (today.month + 2) % 12, 1)
            if today.month >= 11:
                first_payment_date = first_payment_date.replace(year=today.year + 1)
        
        st.write(f"**First Payment Due:** {first_payment_date.strftime('%B 1, %Y')}")
        
        # Get monthly payment from loan structure
        monthly_payment = loan_structure.get('monthly_payment', 0)
        st.write(f"**Monthly Payment Amount:** ${monthly_payment:,.2f}")
        
        # Payment methods
        st.write("**Payment Methods:**")
        st.write("- Online Banking")
        st.write("- Automatic Withdrawal")
        st.write("- Pay by Phone")
        st.write("- Mail Check")
    
    with post_col2:
        st.subheader("Loan Servicing Information")
        
        st.write("**Loan Servicer:** Arose Finance Loan Servicing")
        st.write("**Customer Service:** 1-800-555-1234")
        st.write("**Website:** www.arosefinance.com/servicing")
        st.write("**Email:** servicing@arosefinance.com")
        
        st.info("""
        Your loan servicer will send you information about setting up your account
        and payment options within 5-7 business days.
        """)
    
    # Loan Completion
    if st.session_state.disbursement.get('disbursement_status') == "Complete":
        st.header("Loan Origination Complete")
        
        st.success("🎉 Congratulations! The loan origination process is now complete.")
        
        st.info("""
        Thank you for choosing Arose Finance for your lending needs. Your loan has been
        successfully originated and funds have been disbursed. You will receive your loan
        welcome package in the mail within 7-10 business days.
        
        If you have any questions about your loan, please contact our customer service
        department at 1-800-555-1234 or email us at support@arosefinance.com.
        """)
        
        # Feedback form
        st.subheader("Feedback")
        st.write("We value your feedback on the loan origination process.")
        
        satisfaction = st.slider(
            "How satisfied are you with your loan experience?",
            min_value=1,
            max_value=5,
            value=5,
            step=1,
            key="satisfaction"
        )
        
        feedback = st.text_area(
            "Additional Comments",
            value="",
            key="feedback"
        )
        
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")
            st.balloons() 
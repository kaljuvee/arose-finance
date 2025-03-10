import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import time
import random

st.set_page_config(
    page_title="Approval Process",
    page_icon="✅",
    layout="wide"
)

st.title("Step 7: Approval Process")
st.markdown("Final review and decision making")

# Initialize session state for approval process
if 'approval_process' not in st.session_state:
    st.session_state.approval_process = {
        'approval_status': None,
        'approval_date': None,
        'approved_by': None,
        'approval_notes': None,
        'conditions': [],
        'expiration_date': None
    }

# Check if we have loan structure data
has_loan_structure = 'loan_structure' in st.session_state and st.session_state.loan_structure.get('loan_type')

# Check if we have lender criteria assessment
has_lender_assessment = 'lender_criteria' in st.session_state and st.session_state.lender_criteria.get('overall_assessment')

if not has_loan_structure or not has_lender_assessment:
    st.warning("Complete previous steps before proceeding with the approval process.")
    if not has_loan_structure:
        st.error("Missing loan structure data. Please complete the Loan Structuring step.")
    if not has_lender_assessment:
        st.error("Missing lender criteria assessment. Please complete the Lender Criteria Assessment step.")
else:
    # Get data from session state
    loan_structure = st.session_state.loan_structure
    lender_criteria = st.session_state.lender_criteria
    application_data = st.session_state.application_data if 'application_data' in st.session_state else None
    financial_analysis = st.session_state.financial_analysis if 'financial_analysis' in st.session_state else None
    credit_data = st.session_state.credit_data if 'credit_data' in st.session_state else None
    
    # Application Summary
    st.header("Application Summary")
    
    # Create tabs for different sections of the summary
    summary_tab1, summary_tab2, summary_tab3, summary_tab4 = st.tabs([
        "Borrower Information", 
        "Loan Details", 
        "Financial Assessment",
        "Lender Criteria"
    ])
    
    with summary_tab1:
        if application_data and 'personal_info' in application_data:
            personal_info = application_data['personal_info']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Personal Information")
                st.write(f"**Name:** {personal_info.get('first_name', '')} {personal_info.get('last_name', '')}")
                st.write(f"**Date of Birth:** {personal_info.get('dob', 'Not provided')}")
                st.write(f"**SSN:** {personal_info.get('ssn', 'Not provided')}")
            
            with col2:
                st.subheader("Contact Information")
                st.write(f"**Email:** {personal_info.get('email', 'Not provided')}")
                st.write(f"**Phone:** {personal_info.get('phone', 'Not provided')}")
                st.write(f"**Address:** {personal_info.get('address', 'Not provided')}")
            
            if 'employment_info' in application_data:
                employment_info = application_data['employment_info']
                
                st.subheader("Employment Information")
                st.write(f"**Status:** {employment_info.get('employment_status', 'Not provided')}")
                st.write(f"**Employer:** {employment_info.get('employer_name', 'Not provided')}")
                st.write(f"**Job Title:** {employment_info.get('job_title', 'Not provided')}")
                st.write(f"**Years Employed:** {employment_info.get('years_employed', 'Not provided')}")
        else:
            st.warning("Borrower information not available.")
    
    with summary_tab2:
        if loan_structure:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Loan Structure")
                st.write(f"**Loan Type:** {loan_structure.get('loan_type', 'Not specified')}")
                st.write(f"**Loan Amount:** ${application_data['loan_info'].get('loan_amount', 0):,.2f}")
                st.write(f"**Interest Rate:** {loan_structure.get('interest_rate', 0):.3f}%")
                st.write(f"**Loan Term:** {loan_structure.get('loan_term', 0)} years")
            
            with col2:
                st.subheader("Payment Information")
                st.write(f"**Monthly Payment:** ${loan_structure.get('monthly_payment', 0):,.2f}")
                st.write(f"**Total Interest:** ${loan_structure.get('total_interest', 0):,.2f}")
                st.write(f"**Total Cost:** ${loan_structure.get('total_cost', 0):,.2f}")
                st.write(f"**Cash to Close:** ${loan_structure.get('cash_to_close', 0):,.2f}")
        else:
            st.warning("Loan structure information not available.")
    
    with summary_tab3:
        if financial_analysis:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Income & Expenses")
                st.write(f"**Monthly Income:** ${financial_analysis['income_analysis'].get('total_monthly_income', 0):,.2f}")
                st.write(f"**Monthly Expenses:** ${financial_analysis['expense_analysis'].get('monthly_expenses', 0):,.2f}")
                st.write(f"**Monthly Cash Flow:** ${financial_analysis['cash_flow'].get('monthly_cash_flow', 0):,.2f}")
                st.write(f"**Cash Flow After Loan:** ${financial_analysis['cash_flow'].get('cash_flow_after_loan', 0):,.2f}")
            
            with col2:
                st.subheader("Risk Assessment")
                st.write(f"**Credit Score:** {credit_data['credit_score'] if credit_data else 'Not available'}")
                st.write(f"**DTI Ratio:** {financial_analysis['ratios'].get('dti_ratio', 0):.2f}%")
                st.write(f"**LTV Ratio:** {financial_analysis['ratios'].get('ltv_ratio', 0):.2f}%")
                st.write(f"**Risk Level:** {financial_analysis['risk_assessment'].get('risk_level', 'Not assessed')}")
        else:
            st.warning("Financial analysis information not available.")
    
    with summary_tab4:
        if lender_criteria:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Lender Selection")
                st.write(f"**Selected Lender:** {lender_criteria.get('lender_selection', 'Not specified')}")
                st.write(f"**Assessment:** {lender_criteria.get('overall_assessment', 'Not assessed')}")
                st.write(f"**Recommendation:** {lender_criteria.get('recommendation', 'None')}")
            
            with col2:
                st.subheader("Model Prediction")
                st.write(f"**Approval Confidence:** {lender_criteria.get('model_confidence', 0)*100:.1f}%")
                
                # Create a simple gauge chart for model confidence
                if 'model_confidence' in lender_criteria:
                    confidence = lender_criteria['model_confidence']
                    fig = px.bar(
                        x=[confidence], 
                        y=["Confidence"],
                        orientation='h',
                        range_x=[0, 1],
                        labels={'x': 'Confidence Score'},
                        color=[confidence],
                        color_continuous_scale=['red', 'yellow', 'green']
                    )
                    fig.update_layout(height=100, margin=dict(l=0, r=0, t=0, b=0))
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Lender criteria information not available.")
    
    # Approval Workflow
    st.header("Approval Workflow")
    
    # Define approval roles
    approval_roles = [
        "Loan Officer",
        "Underwriter",
        "Senior Underwriter",
        "Compliance Officer",
        "Branch Manager"
    ]
    
    # Create a workflow status tracker
    workflow_status = {
        "Loan Officer Review": "Completed",
        "Initial Underwriting": "Completed",
        "Document Verification": "Completed",
        "Compliance Review": "In Progress",
        "Final Approval": "Pending"
    }
    
    # Display workflow status
    st.subheader("Workflow Status")
    
    # Create a status dataframe
    status_data = {
        "Step": list(workflow_status.keys()),
        "Status": list(workflow_status.values())
    }
    
    status_df = pd.DataFrame(status_data)
    
    # Add color coding
    status_colors = []
    for status in status_df["Status"]:
        if status == "Completed":
            status_colors.append("#28a745")  # Green
        elif status == "In Progress":
            status_colors.append("#ffc107")  # Yellow
        else:  # Pending
            status_colors.append("#6c757d")  # Gray
    
    status_df["Color"] = status_colors
    
    # Display as a horizontal bar chart
    fig = px.timeline(
        status_df, 
        x_start=0, 
        x_end=[1, 1, 1, 1, 1], 
        y="Step",
        color="Status",
        color_discrete_map={
            "Completed": "#28a745",
            "In Progress": "#ffc107",
            "Pending": "#6c757d"
        }
    )
    
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=200
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Approval Actions
    st.header("Approval Actions")
    
    # Check if already approved
    if st.session_state.approval_process.get('approval_status'):
        st.success(f"✅ Loan {st.session_state.approval_process['approval_status']} on {st.session_state.approval_process['approval_date']}")
        st.info(f"Approved by: {st.session_state.approval_process['approved_by']}")
        
        if st.session_state.approval_process['approval_notes']:
            st.subheader("Approval Notes")
            st.write(st.session_state.approval_process['approval_notes'])
        
        if st.session_state.approval_process['conditions']:
            st.subheader("Approval Conditions")
            for condition in st.session_state.approval_process['conditions']:
                st.warning(f"⚠️ {condition}")
        
        st.subheader("Approval Expiration")
        st.write(f"This approval expires on: {st.session_state.approval_process['expiration_date']}")
        
        # Option to proceed to disbursement
        if st.button("Proceed to Disbursement"):
            st.session_state.approval_process_complete = True
            st.success("Proceeding to Disbursement step.")
            st.balloons()
    else:
        # Approval form
        approval_col1, approval_col2 = st.columns(2)
        
        with approval_col1:
            st.subheader("Approval Decision")
            
            approval_status = st.selectbox(
                "Approval Decision",
                ["Approved", "Approved with Conditions", "Denied"],
                index=0,
                key="approval_status"
            )
            
            approver_role = st.selectbox(
                "Approver Role",
                approval_roles,
                index=1,  # Default to Underwriter
                key="approver_role"
            )
            
            approver_name = st.text_input(
                "Approver Name",
                value="John Smith",  # Placeholder
                key="approver_name"
            )
        
        with approval_col2:
            st.subheader("Approval Details")
            
            approval_notes = st.text_area(
                "Approval Notes",
                value="Loan meets all underwriting guidelines. Borrower has strong credit and income stability.",
                key="approval_notes"
            )
            
            # Calculate expiration date (60 days from now)
            default_expiration = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
            
            expiration_date = st.date_input(
                "Approval Expiration Date",
                value=datetime.strptime(default_expiration, "%Y-%m-%d"),
                key="expiration_date"
            )
        
        # Conditional approval section
        if approval_status == "Approved with Conditions":
            st.subheader("Approval Conditions")
            
            # Suggested conditions based on any issues found in previous steps
            suggested_conditions = []
            
            if financial_analysis and financial_analysis['ratios'].get('dti_ratio', 0) > 36:
                suggested_conditions.append("Verify all income sources with additional documentation")
            
            if financial_analysis and financial_analysis['ratios'].get('ltv_ratio', 0) > 80:
                suggested_conditions.append("Obtain private mortgage insurance (PMI)")
            
            if credit_data and credit_data['credit_score'] < 700:
                suggested_conditions.append("Provide explanation for any derogatory credit items")
            
            if financial_analysis and financial_analysis['cash_flow'].get('cash_flow_after_loan', 0) < 500:
                suggested_conditions.append("Verify cash reserves of at least 3 months of payments")
            
            # Display suggested conditions
            if suggested_conditions:
                st.write("**Suggested Conditions:**")
                conditions_to_add = []
                for condition in suggested_conditions:
                    if st.checkbox(condition, value=True, key=f"condition_{suggested_conditions.index(condition)}"):
                        conditions_to_add.append(condition)
            
            # Allow adding custom conditions
            custom_condition = st.text_input("Add Custom Condition", key="custom_condition")
            if st.button("Add Condition") and custom_condition:
                if 'custom_conditions' not in st.session_state:
                    st.session_state.custom_conditions = []
                st.session_state.custom_conditions.append(custom_condition)
                st.success(f"Added condition: {custom_condition}")
            
            # Display custom conditions
            if 'custom_conditions' in st.session_state and st.session_state.custom_conditions:
                st.write("**Custom Conditions:**")
                for condition in st.session_state.custom_conditions:
                    st.write(f"- {condition}")
        
        # Submit approval
        if st.button("Submit Approval Decision"):
            with st.spinner("Processing approval decision..."):
                # Simulate processing delay
                time.sleep(2)
                
                # Collect all conditions
                all_conditions = []
                
                if approval_status == "Approved with Conditions":
                    # Add suggested conditions that were checked
                    if 'suggested_conditions' in locals():
                        for condition in suggested_conditions:
                            if st.session_state.get(f"condition_{suggested_conditions.index(condition)}", False):
                                all_conditions.append(condition)
                    
                    # Add custom conditions
                    if 'custom_conditions' in st.session_state:
                        all_conditions.extend(st.session_state.custom_conditions)
                
                # Update session state with approval data
                st.session_state.approval_process = {
                    'approval_status': approval_status,
                    'approval_date': datetime.now().strftime("%Y-%m-%d"),
                    'approved_by': f"{approver_name} ({approver_role})",
                    'approval_notes': approval_notes,
                    'conditions': all_conditions,
                    'expiration_date': expiration_date.strftime("%Y-%m-%d")
                }
                
                # Generate approval ID
                approval_id = f"APR-{random.randint(10000, 99999)}"
                st.session_state.approval_process['approval_id'] = approval_id
                
                st.success(f"Approval decision submitted successfully! Approval ID: {approval_id}")
                
                if approval_status == "Approved" or approval_status == "Approved with Conditions":
                    st.balloons()
                    st.session_state.approval_process_complete = True
                    st.success("Please proceed to the Disbursement step.")
                else:
                    st.error("Loan application has been denied. No further action required.")
    
    # Document Generation
    st.header("Document Generation")
    
    doc_col1, doc_col2 = st.columns(2)
    
    with doc_col1:
        st.subheader("Approval Documents")
        
        # Approval letter
        if st.button("Generate Approval Letter"):
            with st.spinner("Generating approval letter..."):
                # Simulate document generation
                time.sleep(2)
                st.success("✅ Approval letter generated successfully!")
                st.download_button(
                    label="Download Approval Letter",
                    data="This is a placeholder for the approval letter content.",
                    file_name="approval_letter.pdf",
                    mime="application/pdf"
                )
        
        # Loan estimate
        if st.button("Generate Loan Estimate"):
            with st.spinner("Generating loan estimate..."):
                # Simulate document generation
                time.sleep(2)
                st.success("✅ Loan estimate generated successfully!")
                st.download_button(
                    label="Download Loan Estimate",
                    data="This is a placeholder for the loan estimate content.",
                    file_name="loan_estimate.pdf",
                    mime="application/pdf"
                )
    
    with doc_col2:
        st.subheader("Closing Documents")
        
        # Closing disclosure
        if st.button("Generate Closing Disclosure"):
            with st.spinner("Generating closing disclosure..."):
                # Simulate document generation
                time.sleep(2)
                st.success("✅ Closing disclosure generated successfully!")
                st.download_button(
                    label="Download Closing Disclosure",
                    data="This is a placeholder for the closing disclosure content.",
                    file_name="closing_disclosure.pdf",
                    mime="application/pdf"
                )
        
        # Note and mortgage/deed
        if st.button("Generate Note and Mortgage/Deed"):
            with st.spinner("Generating note and mortgage/deed..."):
                # Simulate document generation
                time.sleep(3)
                st.success("✅ Note and mortgage/deed generated successfully!")
                st.download_button(
                    label="Download Note",
                    data="This is a placeholder for the note content.",
                    file_name="note.pdf",
                    mime="application/pdf"
                )
                st.download_button(
                    label="Download Mortgage/Deed",
                    data="This is a placeholder for the mortgage/deed content.",
                    file_name="mortgage_deed.pdf",
                    mime="application/pdf"
                ) 
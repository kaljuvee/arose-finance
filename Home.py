import streamlit as st

st.set_page_config(
    page_title="Arose Finance - Loan Origination System",
    page_icon="💰",
    layout="wide"
)

st.title("Arose Finance - Loan Origination System")

st.markdown("""
## Welcome to the Arose Finance Loan Origination System

This application guides you through the complete loan origination process, from initial application to final approval and disbursement.

### Workflow Steps:

1. **Application Intake** - Collect borrower information and loan request details
2. **Document Collection** - Upload and verify required documentation
3. **Credit Bureau Integration** - Retrieve and analyze credit reports
4. **Financial Analysis** - Evaluate borrower's financial health and loan affordability
5. **Lender Criteria Assessment** - Determine if the application meets lender requirements
6. **Loan Structuring** - Configure loan terms based on risk assessment
7. **Approval Process** - Final review and decision making
8. **Disbursement** - Process loan funding and distribution

### Getting Started

Navigate through the workflow using the sidebar menu. Each step will guide you through the required information and actions.

For assistance, please contact support@arosefinance.com
""")

st.sidebar.success("Select a workflow step above.") 
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

st.set_page_config(
    page_title="Document Collection Form",
    page_icon="📄",
    layout="wide"
)

st.title("Step 2: Document Collection Form")
st.markdown("Collect client documents and answers via form to pre-populate fact-find")

# Add demo data checkbox
use_demo_data = st.sidebar.checkbox("Use Demo Data", value=False, key="use_demo_data_step2")

# Check if initial call data exists
if 'application_data' not in st.session_state or 'initial_call' not in st.session_state.application_data:
    if use_demo_data:
        # Create demo application data if it doesn't exist
        st.session_state.application_data = {
            'initial_call': {
                'call_date': datetime.now().strftime("%Y-%m-%d"),
                'call_time': datetime.now().strftime("%H:%M"),
                'call_duration': 30,
                'call_source': "8x8 Work (PC)",
                'broker_name': "John Smith",
                'call_notes': "Client is looking to purchase a new home. They have good credit and stable income."
            },
            'question_set': {
                'loan_purpose': "Home Purchase",
                'property_type': "Single Family Home",
                'property_use': "Primary Residence",
                'loan_amount_range': "$250,000-$500,000",
                'credit_score_range': "700-750",
                'income_type': ["W2 Employment", "Investment Income"]
            },
            'personal_info': {
                'first_name': "Michael",
                'last_name': "Johnson",
                'email': "michael.johnson@example.com",
                'phone': "(555) 123-4567",
                'preferred_contact': "Email",
                'best_time': "Evening"
            },
            'follow_up': {
                'meeting_date': (datetime.now() + pd.Timedelta(days=7)).strftime("%Y-%m-%d"),
                'meeting_time': "14:00",
                'meeting_type': "Video Call (Zoom)",
                'docs_to_request': ["ID/Passport", "Proof of Address", "Bank Statements (3 months)", "Pay Stubs (2 months)", "Tax Returns (2 years)"],
                'additional_info': "Please bring information about any existing debts and current mortgage statements if applicable."
            }
        }
        st.info("Using demo data from Step 1")
    else:
        st.warning("Please complete Step 1: Initial Call Transcript first.")
        st.stop()

# Initialize session state for document tracking and form responses
if 'documents' not in st.session_state:
    st.session_state.documents = {
        'id_verification': None,
        'income_proof': None,
        'bank_statements': None,
        'tax_returns': None,
        'property_documents': None,
        'additional_documents': []
    }

if 'form_responses' not in st.session_state:
    st.session_state.form_responses = {
        'personal_details': {},
        'property_details': {},
        'financial_details': {},
        'employment_details': {}
    }

# Generate demo form responses if using demo data
if use_demo_data and not st.session_state.form_responses.get('personal_details'):
    # Demo personal details
    demo_personal_details = {
        'first_name': "Michael",
        'last_name': "Johnson",
        'dob': "1985-06-15",
        'marital_status': "Married",
        'email': "michael.johnson@example.com",
        'phone': "(555) 123-4567",
        'address': "123 Main Street, Apt 4B, Anytown, CA 94123",
        'years_at_address': 3.5
    }
    
    # Demo property details
    demo_property_details = {
        'property_type': "Single Family Home",
        'property_value': 450000,
        'property_use': "Primary Residence",
        'property_address': "456 Oak Avenue, Anytown, CA 94123"
    }
    
    # Demo financial details
    demo_financial_details = {
        'loan_purpose': "Home Purchase",
        'loan_amount': 360000,
        'down_payment': 90000,
        'credit_score': "700-750",
        'monthly_debt': 1200,
        'bankruptcy': "No"
    }
    
    # Demo employment details
    demo_employment_details = {
        'employment_status': "Employed Full-Time",
        'employer_name': "Acme Corporation",
        'job_title': "Senior Software Engineer",
        'years_employed': 5.5,
        'annual_income': 120000,
        'has_additional_income': True,
        'additional_income_type': ["Investment Income"],
        'additional_income_amount': 1500
    }
    
    # Store demo data in session state
    st.session_state.form_responses = {
        'personal_details': demo_personal_details,
        'property_details': demo_property_details,
        'financial_details': demo_financial_details,
        'employment_details': demo_employment_details
    }
    
    # Simulate document uploads
    st.session_state.documents = {
        'id_verification': "data/uploads/id_verification_demo.jpg",
        'income_proof': "data/uploads/income_proof_demo.pdf",
        'bank_statements': "data/uploads/bank_statements_demo.pdf",
        'tax_returns': "data/uploads/tax_returns_demo.pdf",
        'property_documents': "data/uploads/property_documents_demo.pdf",
        'additional_documents': ["data/uploads/additional_doc1_demo.pdf", "data/uploads/additional_doc2_demo.pdf"]
    }

# Create a function to handle file uploads
def save_uploaded_file(uploaded_file, doc_type):
    if uploaded_file is not None:
        # Create a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Create a directory for uploads if it doesn't exist
        os.makedirs("data/uploads", exist_ok=True)
        # Save the file
        file_extension = uploaded_file.name.split(".")[-1]
        filename = f"data/uploads/{doc_type}_{timestamp}.{file_extension}"
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filename
    return None

# Create tabs for form and documents
tab1, tab2, tab3 = st.tabs(["Client Form", "Document Upload", "Verification Status"])

with tab1:
    st.header("Client Information Form")
    st.info("Please complete all sections of this form. This information will be used to pre-populate your fact-find.")
    
    # Personal Details
    st.subheader("Personal Details")
    col1, col2 = st.columns(2)
    
    # Pre-populate with data from Step 1 if available
    personal_info = st.session_state.application_data.get('personal_info', {})
    form_personal = st.session_state.form_responses.get('personal_details', {})
    
    with col1:
        first_name = st.text_input("First Name", value=form_personal.get('first_name', personal_info.get('first_name', '')), key="form_first_name")
        last_name = st.text_input("Last Name", value=form_personal.get('last_name', personal_info.get('last_name', '')), key="form_last_name")
        dob = st.date_input("Date of Birth", value=datetime.strptime(form_personal.get('dob', '1980-01-01'), "%Y-%m-%d") if form_personal.get('dob') else datetime.now(), key="form_dob")
        marital_status = st.selectbox(
            "Marital Status",
            ["Single", "Married", "Civil Partnership", "Divorced", "Widowed", "Separated"],
            index=["Single", "Married", "Civil Partnership", "Divorced", "Widowed", "Separated"].index(form_personal.get('marital_status', "Single")) if form_personal.get('marital_status') else 0,
            key="form_marital_status"
        )
    
    with col2:
        email = st.text_input("Email Address", value=form_personal.get('email', personal_info.get('email', '')), key="form_email")
        phone = st.text_input("Phone Number", value=form_personal.get('phone', personal_info.get('phone', '')), key="form_phone")
        address = st.text_area("Current Address", value=form_personal.get('address', ''), key="form_address")
        years_at_address = st.number_input("Years at Current Address", min_value=0.0, value=form_personal.get('years_at_address', 0.0), step=0.5, key="form_years_at_address")
    
    # Property Details
    st.subheader("Property Details")
    
    # Pre-populate with data from Step 1 if available
    question_set = st.session_state.application_data.get('question_set', {})
    property_details = st.session_state.form_responses.get('property_details', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        property_type = st.selectbox(
            "Property Type",
            ["Single Family Home", "Multi-Family Home", "Condominium", "Townhouse", "Commercial Property", "Land"],
            index=["Single Family Home", "Multi-Family Home", "Condominium", "Townhouse", "Commercial Property", "Land"].index(property_details.get('property_type', question_set.get('property_type', "Single Family Home"))) if property_details.get('property_type') or question_set.get('property_type') else 0,
            key="form_property_type"
        )
        property_value = st.number_input("Estimated Property Value ($)", min_value=0, value=int(property_details.get('property_value', 0)), step=10000, key="form_property_value")
        
    with col2:
        property_use = st.selectbox(
            "Property Use",
            ["Primary Residence", "Secondary/Vacation Home", "Investment Property", "Business"],
            index=["Primary Residence", "Secondary/Vacation Home", "Investment Property", "Business"].index(property_details.get('property_use', question_set.get('property_use', "Primary Residence"))) if property_details.get('property_use') or question_set.get('property_use') else 0,
            key="form_property_use"
        )
        property_address = st.text_area("Property Address (if different from current address)", value=property_details.get('property_address', ''), key="form_property_address")
    
    # Financial Details
    st.subheader("Financial Details")
    
    financial_details = st.session_state.form_responses.get('financial_details', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        loan_purpose = st.selectbox(
            "Loan Purpose",
            ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation", "Business", "Other"],
            index=["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation", "Business", "Other"].index(financial_details.get('loan_purpose', question_set.get('loan_purpose', "Home Purchase"))) if financial_details.get('loan_purpose') or question_set.get('loan_purpose') else 0,
            key="form_loan_purpose"
        )
        loan_amount = st.number_input("Requested Loan Amount ($)", min_value=0, value=int(financial_details.get('loan_amount', 0)), step=10000, key="form_loan_amount")
        down_payment = st.number_input("Down Payment Amount ($)", min_value=0, value=int(financial_details.get('down_payment', 0)), step=5000, key="form_down_payment")
        
    with col2:
        credit_score = st.selectbox(
            "Credit Score Range",
            ["Below 600", "600-650", "650-700", "700-750", "750+", "Unsure"],
            index=["Below 600", "600-650", "650-700", "700-750", "750+", "Unsure"].index(financial_details.get('credit_score', question_set.get('credit_score_range', "Unsure"))) if financial_details.get('credit_score') or question_set.get('credit_score_range') else 5,
            key="form_credit_score"
        )
        monthly_debt = st.number_input("Current Monthly Debt Payments ($)", min_value=0, value=int(financial_details.get('monthly_debt', 0)), step=100, key="form_monthly_debt")
        bankruptcy = st.selectbox(
            "Have you declared bankruptcy in the last 7 years?",
            ["No", "Yes - Discharged", "Yes - Not Discharged"],
            index=["No", "Yes - Discharged", "Yes - Not Discharged"].index(financial_details.get('bankruptcy', "No")) if financial_details.get('bankruptcy') else 0,
            key="form_bankruptcy"
        )
    
    # Employment Details
    st.subheader("Employment Details")
    
    employment_details = st.session_state.form_responses.get('employment_details', {})
    
    employment_status = st.selectbox(
        "Employment Status",
        ["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed", "Other"],
        index=["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed", "Other"].index(employment_details.get('employment_status', "Employed Full-Time")) if employment_details.get('employment_status') else 0,
        key="form_employment_status"
    )
    
    if employment_status in ["Employed Full-Time", "Employed Part-Time", "Self-Employed"]:
        col1, col2 = st.columns(2)
        
        with col1:
            employer_name = st.text_input("Employer/Business Name", value=employment_details.get('employer_name', ''), key="form_employer_name")
            job_title = st.text_input("Job Title/Position", value=employment_details.get('job_title', ''), key="form_job_title")
            
        with col2:
            years_employed = st.number_input("Years with Current Employer/Business", min_value=0.0, value=float(employment_details.get('years_employed', 0.0)), step=0.5, key="form_years_employed")
            annual_income = st.number_input("Annual Income ($)", min_value=0, value=int(employment_details.get('annual_income', 0)), step=5000, key="form_annual_income")
    
    # Additional Income
    st.subheader("Additional Income (if applicable)")
    has_additional_income = st.checkbox("I have additional sources of income", value=employment_details.get('has_additional_income', False), key="form_has_additional_income")
    
    if has_additional_income:
        additional_income_type = st.multiselect(
            "Additional Income Sources",
            ["Rental Income", "Investment Income", "Pension", "Social Security", "Alimony/Child Support", "Other"],
            default=employment_details.get('additional_income_type', []),
            key="form_additional_income_type"
        )
        additional_income_amount = st.number_input("Total Additional Monthly Income ($)", min_value=0, value=int(employment_details.get('additional_income_amount', 0)), step=100, key="form_additional_income_amount")

with tab2:
    st.header("Document Upload")
    st.info("Please upload all required documents. These documents will be used to verify the information provided in the form.")
    
    # Get requested documents from Step 1
    requested_docs = st.session_state.application_data.get('follow_up', {}).get('docs_to_request', [])
    
    # Display requested documents with a checkmark
    if requested_docs:
        st.subheader("Requested Documents")
        for doc in requested_docs:
            st.markdown(f"✓ {doc}")
    
    # ID Verification
    st.subheader("Identification")
    
    # Display demo document status if using demo data
    if use_demo_data and st.session_state.documents.get('id_verification'):
        st.success("✅ ID Verification document uploaded (Demo)")
    else:
        id_doc = st.file_uploader("Government-issued ID (Driver's License, Passport, etc.)", 
                                type=["pdf", "jpg", "jpeg", "png"], 
                                key="id_verification")
        if id_doc:
            st.session_state.documents['id_verification'] = save_uploaded_file(id_doc, "id_verification")
            st.success(f"✅ {id_doc.name} uploaded successfully!")
    
    # Income Proof
    st.subheader("Income Verification")
    
    # Display demo document status if using demo data
    if use_demo_data and st.session_state.documents.get('income_proof'):
        st.success("✅ Income Proof document uploaded (Demo)")
    else:
        income_doc = st.file_uploader("Recent Pay Stubs (last 2 months)", 
                                    type=["pdf", "jpg", "jpeg", "png"], 
                                    key="income_proof")
        if income_doc:
            st.session_state.documents['income_proof'] = save_uploaded_file(income_doc, "income_proof")
            st.success(f"✅ {income_doc.name} uploaded successfully!")
    
    # Bank Statements
    st.subheader("Financial Documents")
    
    # Display demo document status if using demo data
    if use_demo_data and st.session_state.documents.get('bank_statements'):
        st.success("✅ Bank Statements uploaded (Demo)")
    else:
        bank_doc = st.file_uploader("Bank Statements (last 3 months)", 
                                type=["pdf", "jpg", "jpeg", "png"], 
                                key="bank_statements")
        if bank_doc:
            st.session_state.documents['bank_statements'] = save_uploaded_file(bank_doc, "bank_statements")
            st.success(f"✅ {bank_doc.name} uploaded successfully!")
    
    # Tax Returns
    # Display demo document status if using demo data
    if use_demo_data and st.session_state.documents.get('tax_returns'):
        st.success("✅ Tax Returns uploaded (Demo)")
    else:
        tax_doc = st.file_uploader("Tax Returns (last 2 years)", 
                                type=["pdf", "jpg", "jpeg", "png"], 
                                key="tax_returns")
        if tax_doc:
            st.session_state.documents['tax_returns'] = save_uploaded_file(tax_doc, "tax_returns")
            st.success(f"✅ {tax_doc.name} uploaded successfully!")
    
    # Property Documents (if applicable)
    st.subheader("Property Documents (if applicable)")
    
    # Display demo document status if using demo data
    if use_demo_data and st.session_state.documents.get('property_documents'):
        st.success("✅ Property Documents uploaded (Demo)")
    else:
        property_doc = st.file_uploader("Property Documentation (Deed, Title, etc.)", 
                                    type=["pdf", "jpg", "jpeg", "png"], 
                                    key="property_documents")
        if property_doc:
            st.session_state.documents['property_documents'] = save_uploaded_file(property_doc, "property_documents")
            st.success(f"✅ {property_doc.name} uploaded successfully!")
    
    # Additional Documents
    st.subheader("Additional Documents (Optional)")
    
    # Display demo document status if using demo data
    if use_demo_data and st.session_state.documents.get('additional_documents'):
        st.success(f"✅ {len(st.session_state.documents['additional_documents'])} Additional Documents uploaded (Demo)")
    else:
        additional_doc = st.file_uploader("Upload any additional supporting documents", 
                                        type=["pdf", "jpg", "jpeg", "png"], 
                                        key="additional_documents",
                                        accept_multiple_files=True)
        if additional_doc:
            for doc in additional_doc:
                file_path = save_uploaded_file(doc, "additional")
                if file_path:
                    st.session_state.documents['additional_documents'].append(file_path)
                    st.success(f"✅ {doc.name} uploaded successfully!")

with tab3:
    st.header("Verification Status")
    
    # Form Completion Status
    st.subheader("Form Completion Status")
    
    # Check if essential form fields are filled
    form_fields = {
        "Personal Details": first_name and last_name and email and phone,
        "Property Details": property_type and property_value,
        "Financial Details": loan_purpose and loan_amount,
        "Employment Details": employment_status
    }
    
    form_status = pd.DataFrame({
        "Section": list(form_fields.keys()),
        "Status": ["Complete" if status else "Incomplete" for status in form_fields.values()]
    })
    
    st.dataframe(form_status, use_container_width=True)
    
    # Document Verification Status
    st.subheader("Document Verification Status")
    
    # Create a dataframe to display document status
    doc_status = {
        "Document Type": ["Identification", "Income Verification", "Bank Statements", "Tax Returns", "Property Documents"],
        "Status": [
            "Uploaded" if st.session_state.documents['id_verification'] else "Pending",
            "Uploaded" if st.session_state.documents['income_proof'] else "Pending",
            "Uploaded" if st.session_state.documents['bank_statements'] else "Pending",
            "Uploaded" if st.session_state.documents['tax_returns'] else "Pending",
            "Uploaded" if st.session_state.documents['property_documents'] else "N/A (if applicable)"
        ]
    }
    
    status_df = pd.DataFrame(doc_status)
    st.dataframe(status_df, use_container_width=True)
    
    # Check if all required documents are uploaded and form is complete
    required_docs = ['id_verification', 'income_proof', 'bank_statements', 'tax_returns']
    all_required_uploaded = all(st.session_state.documents[doc] is not None for doc in required_docs)
    all_form_complete = all(form_fields.values())
    
    if all_required_uploaded and all_form_complete:
        st.success("All required documents have been uploaded and form is complete. You can proceed to the next step.")
    else:
        if not all_required_uploaded:
            st.warning("Please upload all required documents before proceeding.")
        if not all_form_complete:
            st.warning("Please complete all sections of the form before proceeding.")

# Save and Continue Button
if st.button("Save and Continue"):
    # Save form responses
    st.session_state.form_responses['personal_details'] = {
        'first_name': first_name,
        'last_name': last_name,
        'dob': dob.strftime("%Y-%m-%d") if dob else None,
        'marital_status': marital_status,
        'email': email,
        'phone': phone,
        'address': address,
        'years_at_address': years_at_address
    }
    
    st.session_state.form_responses['property_details'] = {
        'property_type': property_type,
        'property_value': property_value,
        'property_use': property_use,
        'property_address': property_address
    }
    
    st.session_state.form_responses['financial_details'] = {
        'loan_purpose': loan_purpose,
        'loan_amount': loan_amount,
        'down_payment': down_payment,
        'credit_score': credit_score,
        'monthly_debt': monthly_debt,
        'bankruptcy': bankruptcy
    }
    
    st.session_state.form_responses['employment_details'] = {
        'employment_status': employment_status,
        'employer_name': employer_name if 'employer_name' in locals() else None,
        'job_title': job_title if 'job_title' in locals() else None,
        'years_employed': years_employed if 'years_employed' in locals() else None,
        'annual_income': annual_income if 'annual_income' in locals() else None,
        'has_additional_income': has_additional_income if 'has_additional_income' in locals() else False,
        'additional_income_type': additional_income_type if 'additional_income_type' in locals() else None,
        'additional_income_amount': additional_income_amount if 'additional_income_amount' in locals() else None
    }
    
    # Check if all required documents are uploaded and form is complete
    if all_required_uploaded and all_form_complete:
        st.session_state.document_collection_complete = True
        
        # Generate outputs
        st.session_state.outputs = {
            'fact_find_prepopulated': True,
            'fact_find_question_set_enriched': True
        }
        
        st.success("Form and documents saved successfully! Fact-find has been pre-populated with your information.")
        
        # Display outputs
        st.subheader("Outputs Generated")
        st.markdown("✅ Fact-find pre-populated with your information")
        st.markdown("✅ Fact-find question set enriched based on your responses")
        
        st.balloons()
    else:
        if not all_required_uploaded:
            st.error("Please upload all required documents before proceeding.")
        if not all_form_complete:
            st.error("Please complete all sections of the form before proceeding.") 
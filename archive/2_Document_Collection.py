import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Document Collection",
    page_icon="📄",
    layout="wide"
)

st.title("Step 2: Document Collection")
st.markdown("Upload and verify required documentation")

# Initialize session state for document tracking
if 'documents' not in st.session_state:
    st.session_state.documents = {
        'id_verification': None,
        'income_proof': None,
        'bank_statements': None,
        'tax_returns': None,
        'property_documents': None,
        'additional_documents': []
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

# Required Documents Section
st.header("Required Documents")
st.info("Please upload the following required documents in PDF, JPG, or PNG format.")

col1, col2 = st.columns(2)

with col1:
    # ID Verification
    st.subheader("Identification")
    id_doc = st.file_uploader("Government-issued ID (Driver's License, Passport, etc.)", 
                              type=["pdf", "jpg", "jpeg", "png"], 
                              key="id_verification")
    if id_doc:
        st.session_state.documents['id_verification'] = save_uploaded_file(id_doc, "id_verification")
        st.success(f"✅ {id_doc.name} uploaded successfully!")
    
    # Income Proof
    st.subheader("Income Verification")
    income_doc = st.file_uploader("Recent Pay Stubs (last 2 months)", 
                                 type=["pdf", "jpg", "jpeg", "png"], 
                                 key="income_proof")
    if income_doc:
        st.session_state.documents['income_proof'] = save_uploaded_file(income_doc, "income_proof")
        st.success(f"✅ {income_doc.name} uploaded successfully!")

with col2:
    # Bank Statements
    st.subheader("Financial Documents")
    bank_doc = st.file_uploader("Bank Statements (last 3 months)", 
                               type=["pdf", "jpg", "jpeg", "png"], 
                               key="bank_statements")
    if bank_doc:
        st.session_state.documents['bank_statements'] = save_uploaded_file(bank_doc, "bank_statements")
        st.success(f"✅ {bank_doc.name} uploaded successfully!")
    
    # Tax Returns
    tax_doc = st.file_uploader("Tax Returns (last 2 years)", 
                              type=["pdf", "jpg", "jpeg", "png"], 
                              key="tax_returns")
    if tax_doc:
        st.session_state.documents['tax_returns'] = save_uploaded_file(tax_doc, "tax_returns")
        st.success(f"✅ {tax_doc.name} uploaded successfully!")

# Property Documents (if applicable)
st.subheader("Property Documents (if applicable)")
property_doc = st.file_uploader("Property Documentation (Deed, Title, etc.)", 
                               type=["pdf", "jpg", "jpeg", "png"], 
                               key="property_documents")
if property_doc:
    st.session_state.documents['property_documents'] = save_uploaded_file(property_doc, "property_documents")
    st.success(f"✅ {property_doc.name} uploaded successfully!")

# Additional Documents
st.subheader("Additional Documents (Optional)")
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

# Document Verification Status
st.header("Document Verification Status")

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

# Check if all required documents are uploaded
required_docs = ['id_verification', 'income_proof', 'bank_statements', 'tax_returns']
all_required_uploaded = all(st.session_state.documents[doc] is not None for doc in required_docs)

if all_required_uploaded:
    st.success("All required documents have been uploaded. You can proceed to the next step.")
else:
    st.warning("Please upload all required documents before proceeding to the next step.")

# Save and Continue Button
if st.button("Save and Continue"):
    if all_required_uploaded:
        st.session_state.document_collection_complete = True
        st.success("Documents saved successfully! Please proceed to the next step.")
        st.balloons()
    else:
        st.error("Please upload all required documents before proceeding.") 
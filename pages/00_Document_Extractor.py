import streamlit as st
import os
import tempfile
import pandas as pd
import PyPDF2
import openai
from openai import OpenAI
import json
import re
from io import StringIO
from PIL import Image
from utils import load_api_keys

st.set_page_config(
    page_title="KYC Document Verification",
    page_icon="🔍",
    layout="wide"
)

st.title("KYC Document Verification")
st.markdown("Upload bank statements and utility bills for verification and analysis")

# Load API keys from .env file
api_keys_loaded = load_api_keys()

# Initialize session state variables if they don't exist
if 'extracted_bank_statement_data' not in st.session_state:
    st.session_state.extracted_bank_statement_data = None
if 'extracted_utility_bill_data' not in st.session_state:
    st.session_state.extracted_utility_bill_data = None
if 'verification_results' not in st.session_state:
    st.session_state.verification_results = None
if 'saved_analyses' not in st.session_state:
    st.session_state.saved_analyses = []
if 'use_demo_data' not in st.session_state:
    st.session_state.use_demo_data = False

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(pdf_file.getvalue())
        temp_path = temp_file.name
    
    text = ""
    with open(temp_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    
    os.unlink(temp_path)
    return text

# Function to extract text from PDF file path
def extract_text_from_pdf_path(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    
    return text

# Function to extract data using OpenAI
def extract_data_with_openai(text, document_type):
    client = OpenAI(api_key=st.session_state.openai_api_key)
    
    # Load the system prompt
    with open("prompts/kyc_documents_prompt.md", "r") as f:
        system_prompt = f.read()
    
    user_prompt = f"""
    Extract all relevant information from this {document_type} document. 
    The document text is provided below:
    
    {text}
    
    Return the extracted information as a JSON object with all relevant fields as specified in the guidelines.
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

# Function to verify KYC documents
def verify_documents(bank_statement_data, utility_bill_data, image_analyses=None):
    client = OpenAI(api_key=st.session_state.openai_api_key)
    
    # Load the system prompt
    with open("prompts/kyc_documents_prompt.md", "r") as f:
        system_prompt = f.read()
    
    # Prepare image analyses text if available
    image_analyses_text = ""
    if image_analyses and len(image_analyses) > 0:
        image_analyses_text = "IMAGE ANALYSES:\n"
        for i, analysis in enumerate(image_analyses):
            image_analyses_text += f"\nImage {i+1}: {analysis['image_name']}\n"
            image_analyses_text += f"Analysis Type: {analysis['analysis_type']}\n"
            image_analyses_text += f"Model Used: {analysis['model_used']}\n"
            image_analyses_text += f"Analysis Result:\n{analysis['analysis_result']}\n"
            image_analyses_text += "-" * 50 + "\n"
    
    user_prompt = f"""
    Compare and verify the following bank statement and utility bill data:
    
    BANK STATEMENT DATA:
    {json.dumps(bank_statement_data, indent=2)}
    
    UTILITY BILL DATA:
    {json.dumps(utility_bill_data, indent=2)}
    
    {image_analyses_text}
    
    Provide a detailed verification report highlighting any inconsistencies or issues.
    Return the results as a JSON object with the following structure:
    {{
        "document_summary": "Brief overview of the documents analyzed",
        "verification_results": [
            {{
                "field": "Field name (like name, address, etc)",
                "bank_statement_value": "Value from bank statement",
                "utility_bill_value": "Value from utility bill",
                "match": true/false,
                "notes": "Any notes about this comparison"
            }}
        ],
        "discrepancies": [
            {{
                "field": "Field with discrepancy",
                "description": "Description of the issue",
                "severity": "high/medium/low",
                "potential_risk": "Description of potential fraud risk if applicable"
            }}
        ],
        "recommendations": [
            "Recommendation 1",
            "Recommendation 2"
        ],
        "verification_status": "approved/rejected/needs_review",
        "confidence_score": "A number between 0-100 indicating confidence in verification"
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

# Function to convert JSON to DataFrame
def json_to_df(json_data):
    """Convert JSON data to a pandas DataFrame for display"""
    # Flatten the JSON if it's nested
    flat_data = {}
    
    def flatten(data, prefix=""):
        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{prefix}{key}" if prefix else key
                if isinstance(value, (dict, list)) and not isinstance(value, str):
                    flatten(value, f"{new_key}.")
                else:
                    flat_data[new_key] = value
        elif isinstance(data, list) and not isinstance(data, str):
            for i, item in enumerate(data):
                flatten(item, f"{prefix}[{i}].")
    
    flatten(json_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(flat_data.items(), columns=["Field", "Value"])
    return df

# API Key input
with st.sidebar:
    st.header("API Keys")
    
    # Show status of loaded API keys
    if api_keys_loaded['openai_api_key']:
        st.success("OpenAI API key loaded from .env file")
    else:
        st.warning("OpenAI API key not found in .env file")
    
    # Optional override for OpenAI API key
    st.subheader("Override API Key (Optional)")
    openai_api_key = st.text_input("Enter OpenAI API key to override", type="password")
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.success("API key override applied!")
    
    # Demo data checkbox
    st.header("Demo Options")
    use_demo = st.checkbox("Use demo data", value=st.session_state.use_demo_data)
    if use_demo != st.session_state.use_demo_data:
        st.session_state.use_demo_data = use_demo
        # Reset extracted data when toggling demo mode
        st.session_state.extracted_bank_statement_data = None
        st.session_state.extracted_utility_bill_data = None
        st.session_state.verification_results = None
        st.rerun()

# Main content
if 'openai_api_key' in st.session_state:
    # Create tabs for different sections
    tabs = st.tabs(["Document Analysis", "Image Analysis Integration", "Verification Results"])
    
    with tabs[0]:
        # Demo data section
        if st.session_state.use_demo_data:
            st.info("Using demo data from the data directory")
            
            # Display demo files
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("Bank Statement")
                st.markdown("Using: **sample-bank-statement.pdf**")
                
                if st.button("Extract Bank Statement Data"):
                    with st.spinner("Analyzing bank statement with AI..."):
                        try:
                            bank_statement_text = extract_text_from_pdf_path("data/sample-bank-statement.pdf")
                            extracted_bank_statement_data = extract_data_with_openai(bank_statement_text, "bank statement")
                            st.session_state.extracted_bank_statement_data = extracted_bank_statement_data
                            st.success("Bank statement data extracted successfully!")
                            
                            # Display extracted data as DataFrame
                            st.subheader("Extracted Bank Statement Data")
                            bank_statement_df = json_to_df(extracted_bank_statement_data)
                            st.dataframe(bank_statement_df, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error extracting bank statement data: {str(e)}")
            
            with col2:
                st.header("Utility Bill")
                st.markdown("Using: **sample-utility-bill.pdf**")
                
                if st.button("Extract Utility Bill Data"):
                    with st.spinner("Analyzing utility bill with AI..."):
                        try:
                            utility_bill_text = extract_text_from_pdf_path("data/sample-utility-bill.pdf")
                            extracted_utility_bill_data = extract_data_with_openai(utility_bill_text, "utility bill")
                            st.session_state.extracted_utility_bill_data = extracted_utility_bill_data
                            st.success("Utility bill data extracted successfully!")
                            
                            # Display extracted data as DataFrame
                            st.subheader("Extracted Utility Bill Data")
                            utility_bill_df = json_to_df(extracted_utility_bill_data)
                            st.dataframe(utility_bill_df, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error extracting utility bill data: {str(e)}")
        
        # User upload section
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("Upload Bank Statement")
                bank_statement_file = st.file_uploader("Upload a bank statement document", type=["pdf"], key="bank_statement_uploader")
                
                if bank_statement_file:
                    with st.spinner("Extracting text from bank statement..."):
                        bank_statement_text = extract_text_from_pdf(bank_statement_file)
                        st.session_state.bank_statement_text = bank_statement_text
                        
                    if st.button("Extract Bank Statement Data"):
                        with st.spinner("Analyzing bank statement with AI..."):
                            try:
                                extracted_bank_statement_data = extract_data_with_openai(bank_statement_text, "bank statement")
                                st.session_state.extracted_bank_statement_data = extracted_bank_statement_data
                                st.success("Bank statement data extracted successfully!")
                                
                                # Display extracted data as DataFrame
                                st.subheader("Extracted Bank Statement Data")
                                bank_statement_df = json_to_df(extracted_bank_statement_data)
                                st.dataframe(bank_statement_df, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error extracting bank statement data: {str(e)}")
            
            with col2:
                st.header("Upload Utility Bill")
                utility_bill_file = st.file_uploader("Upload a utility bill document", type=["pdf"], key="utility_bill_uploader")
                
                if utility_bill_file:
                    with st.spinner("Extracting text from utility bill..."):
                        utility_bill_text = extract_text_from_pdf(utility_bill_file)
                        st.session_state.utility_bill_text = utility_bill_text
                        
                    if st.button("Extract Utility Bill Data"):
                        with st.spinner("Analyzing utility bill with AI..."):
                            try:
                                extracted_utility_bill_data = extract_data_with_openai(utility_bill_text, "utility bill")
                                st.session_state.extracted_utility_bill_data = extracted_utility_bill_data
                                st.success("Utility bill data extracted successfully!")
                                
                                # Display extracted data as DataFrame
                                st.subheader("Extracted Utility Bill Data")
                                utility_bill_df = json_to_df(extracted_utility_bill_data)
                                st.dataframe(utility_bill_df, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error extracting utility bill data: {str(e)}")
    
    with tabs[1]:
        st.header("Image Analysis Integration")
        
        if len(st.session_state.saved_analyses) > 0:
            st.success(f"You have {len(st.session_state.saved_analyses)} saved image analyses available")
            
            # Display saved analyses
            for i, analysis in enumerate(st.session_state.saved_analyses):
                with st.expander(f"Image Analysis {i+1}: {analysis['image_name']} ({analysis['timestamp']})"):
                    st.write(f"**Analysis Type:** {analysis['analysis_type']}")
                    st.write(f"**Model Used:** {analysis['model_used']}")
                    st.markdown("**Analysis Result:**")
                    st.markdown(analysis['analysis_result'])
            
            # Select analyses to include
            st.subheader("Select Analyses to Include in KYC Verification")
            selected_analyses = []
            for i, analysis in enumerate(st.session_state.saved_analyses):
                if st.checkbox(f"Include {analysis['image_name']} in verification", key=f"include_analysis_{i}"):
                    selected_analyses.append(analysis)
            
            st.session_state.selected_analyses = selected_analyses
            
            if len(selected_analyses) > 0:
                st.success(f"Selected {len(selected_analyses)} analyses for inclusion in KYC verification")
        else:
            st.info("No saved image analyses available. Go to the Image Detection page to analyze images and save the results.")
            st.markdown("""
            ### How to add image analyses:
            1. Navigate to the **Image Detection** page
            2. Upload and analyze an image (e.g., ID documents, signatures)
            3. Click the **Save Analysis for KYC** button
            4. Return to this page to include the analysis in your verification
            """)
    
    with tabs[2]:
        st.header("Verification Results")
        
        # Verify button
        if (st.session_state.extracted_bank_statement_data and 
            st.session_state.extracted_utility_bill_data):
            
            selected_analyses = st.session_state.get('selected_analyses', [])
            include_images = len(selected_analyses) > 0
            
            verify_button_text = "Verify Documents"
            if include_images:
                verify_button_text += f" (Including {len(selected_analyses)} Image Analyses)"
                
            if st.button(verify_button_text):
                with st.spinner("Verifying documents..."):
                    try:
                        verification_results = verify_documents(
                            st.session_state.extracted_bank_statement_data,
                            st.session_state.extracted_utility_bill_data,
                            selected_analyses if include_images else None
                        )
                        st.session_state.verification_results = verification_results
                        st.success("Verification completed!")
                    except Exception as e:
                        st.error(f"Error verifying documents: {str(e)}")
        else:
            missing = []
            if not st.session_state.extracted_bank_statement_data:
                missing.append("Bank Statement")
            if not st.session_state.extracted_utility_bill_data:
                missing.append("Utility Bill")
            
            if missing:
                st.warning(f"Please extract data from all documents before verifying. Missing: {', '.join(missing)}")
        
        # Display results
        if st.session_state.verification_results:
            # Document Summary
            st.subheader("Document Summary")
            st.write(st.session_state.verification_results.get("document_summary", "No summary available"))
            
            # Verification Status
            verification_status = st.session_state.verification_results.get("verification_status", "needs_review")
            confidence_score = st.session_state.verification_results.get("confidence_score", "N/A")
            
            status_col1, status_col2 = st.columns(2)
            with status_col1:
                if verification_status == "approved":
                    st.success(f"✅ Verification Status: APPROVED")
                elif verification_status == "rejected":
                    st.error(f"❌ Verification Status: REJECTED")
                else:
                    st.warning(f"⚠️ Verification Status: NEEDS REVIEW")
            
            with status_col2:
                st.metric("Confidence Score", confidence_score)
            
            # Verification Table
            st.subheader("Verification Details")
            if "verification_results" in st.session_state.verification_results:
                verification_df = pd.DataFrame(st.session_state.verification_results["verification_results"])
                
                # Apply styling to highlight mismatches
                def highlight_mismatches(row):
                    if not row['match']:
                        return ['background-color: #ffcccc'] * len(row)
                    return [''] * len(row)
                
                st.dataframe(verification_df.style.apply(highlight_mismatches, axis=1), use_container_width=True)
            else:
                st.write("No verification data available")
            
            # Discrepancies
            st.subheader("Discrepancies")
            if "discrepancies" in st.session_state.verification_results and st.session_state.verification_results["discrepancies"]:
                discrepancies_df = pd.DataFrame(st.session_state.verification_results["discrepancies"])
                
                # Apply styling based on severity
                def highlight_severity(row):
                    if row['severity'].lower() == 'high':
                        return ['background-color: #ffcccc'] * len(row)
                    elif row['severity'].lower() == 'medium':
                        return ['background-color: #ffffcc'] * len(row)
                    return [''] * len(row)
                
                st.dataframe(discrepancies_df.style.apply(highlight_severity, axis=1), use_container_width=True)
            else:
                st.write("No discrepancies found")
            
            # Recommendations
            st.subheader("Recommendations")
            if "recommendations" in st.session_state.verification_results:
                for i, rec in enumerate(st.session_state.verification_results["recommendations"]):
                    st.write(f"{i+1}. {rec}")
            else:
                st.write("No recommendations available")
            
            # Export results
            st.subheader("Export Results")
            if st.download_button(
                label="Download Verification Report",
                data=json.dumps(st.session_state.verification_results, indent=2),
                file_name="kyc_verification_report.json",
                mime="application/json"
            ):
                st.success("Report downloaded successfully!")
else:
    st.warning("OpenAI API key is required. Please add it to your .env file or enter it in the sidebar.") 
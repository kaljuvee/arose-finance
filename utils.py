import os
import streamlit as st
from dotenv import load_dotenv

def load_api_keys():
    """
    Load API keys from .env file and store them in session state
    Returns a dictionary with status of each key
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API keys from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    # Store API keys in session state if they exist
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
    
    # Return status of API keys
    return {
        "openai_api_key": openai_api_key is not None
    }

def ensure_dir(directory):
    """
    Create directory if it doesn't exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def extract_personal_info_from_documents(extracted_data):
    """
    Extract personal information from document extraction results
    Returns a dictionary with consolidated personal information
    """
    personal_info = {}
    
    # Loop through all extracted document data
    for doc_type, data in extracted_data.items():
        if not data:
            continue
            
        extracted = data.get("extracted_data", {})
        
        # Extract name from various document types
        if "full_name" in extracted and not personal_info.get("full_name"):
            personal_info["full_name"] = extracted["full_name"]
        elif "account_holder" in extracted and not personal_info.get("full_name"):
            personal_info["full_name"] = extracted["account_holder"]
        elif "employee_name" in extracted and not personal_info.get("full_name"):
            personal_info["full_name"] = extracted["employee_name"]
        elif "taxpayer_name" in extracted and not personal_info.get("full_name"):
            personal_info["full_name"] = extracted["taxpayer_name"]
            
        # Extract address
        if "billing_address" in extracted and not personal_info.get("address"):
            personal_info["address"] = extracted["billing_address"]
            
        # Extract date of birth
        if "date_of_birth" in extracted and not personal_info.get("date_of_birth"):
            personal_info["date_of_birth"] = extracted["date_of_birth"]
            
        # Extract employment details
        if "employer_name" in extracted and not personal_info.get("employer_name"):
            personal_info["employer_name"] = extracted["employer_name"]
            
        # Extract income information
        if "gross_income" in extracted and not personal_info.get("annual_income"):
            # Convert to annual if it's a pay stub
            pay_period = extracted.get("pay_period", "").lower()
            if "month" in pay_period:
                personal_info["annual_income"] = float(extracted["gross_income"]) * 12
            elif "bi-week" in pay_period or "fortnight" in pay_period:
                personal_info["annual_income"] = float(extracted["gross_income"]) * 26
            elif "week" in pay_period:
                personal_info["annual_income"] = float(extracted["gross_income"]) * 52
            else:
                personal_info["annual_income"] = float(extracted["gross_income"])
                
        # Extract account information from bank statements
        if doc_type == "bank_statements" and "account_number" in extracted:
            personal_info["account_number"] = extracted["account_number"]
            personal_info["bank_name"] = extracted.get("bank_name")
            
    # Split full name into first and last name if possible
    if "full_name" in personal_info and " " in personal_info["full_name"]:
        name_parts = personal_info["full_name"].split(" ", 1)
        personal_info["first_name"] = name_parts[0]
        personal_info["last_name"] = name_parts[1]
            
    return personal_info 
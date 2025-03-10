import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.inspection import permutation_importance
import joblib
import os
from datetime import datetime

# Check if user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

st.set_page_config(
    page_title="Lender Matching",
    page_icon="🎯",
    layout="wide"
)

st.title("Step 5: Lender Matching")
st.markdown("Match the client profile to lenders with probability of success")

# Add demo data checkbox
use_demo_data = st.sidebar.checkbox("Use Demo Data", value=True, key="use_demo_data_step5")

# Initialize session state for lender matching
if 'lender_matching' not in st.session_state:
    st.session_state.lender_matching = {
        'matched_lenders': [],
        'research_matrix_results': {},
        'unstructured_criteria_results': {},
        'final_probabilities': {}
    }

# Load lender criteria CSV
def load_lender_criteria_csv():
    # Check if the data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Path to the lender criteria CSV
    csv_path = "data/lender_criteria.csv"
    
    try:
        # Try to load the CSV file
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        # If file doesn't exist, create a sample DataFrame with the same structure
        # as the attached CSV but with fewer rows for demonstration
        st.warning("Lender criteria CSV file not found. Creating a sample file.")
        
        # Create a simplified version with just a few lenders
        sample_data = {
            "Lender": ["Lender 1", "Lender 2", "Lender 3", "Lender 4", "Lender 5"],
            "England": ["Y", "Y", "Y", "Y", "Y"],
            "Wales": ["Y", "Y", "Y", "Y", "Y"],
            "Scotland": ["N", "N", "Y", "Y", "Y"],
            "Max LTV": [75, 70, 70, 70, 70],
            "Minimum Loan Size": [50000, 100000, 300000, 20000, 2500000],
            "Maximum Loan Size": [3000000, 10000000, 8000000, 3000000, 10000000],
            "Interest Rate": [0.85, 0.95, 1.10, 1.00, 0.90]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(csv_path, index=False)
        return df

# Load lender criteria
lender_criteria_df = load_lender_criteria_csv()

# Generate demo client profile if using demo data
if use_demo_data:
    # Demo client profile
    demo_client_profile = {
        'first_name': "Michael",
        'last_name': "Johnson",
        'email': "michael.johnson@example.com",
        'phone': "(555) 123-4567"
    }
    
    # Demo loan requirements
    demo_loan_requirements = {
        'loan_purpose': "Home Purchase",
        'loan_amount': 360000,
        'down_payment': 90000,
        'loan_term_preference': "30 years"
    }
    
    # Demo property details
    demo_property_details = {
        'property_type': "Single Family Home",
        'property_value': 450000,
        'property_use': "Primary Residence",
        'property_location': "England"
    }
    
    # Demo financial profile
    demo_financial_profile = {
        'employment_status': "Employed Full-Time",
        'employer_name': "Acme Corporation",
        'job_title': "Senior Software Engineer",
        'years_employed': 5.5,
        'annual_income': 120000,
        'credit_score': "700-750",
        'bankruptcy': "No",
        'existing_mortgage': 0,
        'credit_card_debt': 5000,
        'other_loans': 500
    }
    
    # Store demo data in session state
    if 'verified_profile' not in st.session_state:
        st.session_state.verified_profile = {
            'client_profile': demo_client_profile,
            'loan_requirements': demo_loan_requirements,
            'property_details': demo_property_details,
            'financial_profile': demo_financial_profile
        }

# Get client profile
client_profile = st.session_state.verified_profile['client_profile'] if 'verified_profile' in st.session_state else {}
loan_requirements = st.session_state.verified_profile['loan_requirements'] if 'verified_profile' in st.session_state else {}
property_details = st.session_state.verified_profile['property_details'] if 'verified_profile' in st.session_state else {}
financial_profile = st.session_state.verified_profile['financial_profile'] if 'verified_profile' in st.session_state else {}

# Display client profile summary
st.header("Client Profile Summary")
client_col1, client_col2 = st.columns(2)

with client_col1:
    st.subheader("Client Information")
    st.write(f"**Name:** {client_profile.get('first_name', '')} {client_profile.get('last_name', '')}")
    st.write(f"**Email:** {client_profile.get('email', '')}")
    st.write(f"**Phone:** {client_profile.get('phone', '')}")
    
    st.subheader("Loan Requirements")
    st.write(f"**Loan Purpose:** {loan_requirements.get('loan_purpose', '')}")
    st.write(f"**Loan Amount:** ${loan_requirements.get('loan_amount', 0):,}")
    st.write(f"**Down Payment:** ${loan_requirements.get('down_payment', 0):,}")
    st.write(f"**Preferred Term:** {loan_requirements.get('loan_term_preference', '')}")

with client_col2:
    st.subheader("Property Details")
    st.write(f"**Property Type:** {property_details.get('property_type', '')}")
    st.write(f"**Property Value:** ${property_details.get('property_value', 0):,}")
    st.write(f"**Property Use:** {property_details.get('property_use', '')}")
    st.write(f"**Property Location:** {property_details.get('property_location', 'England')}")
    
    st.subheader("Financial Profile")
    st.write(f"**Employment:** {financial_profile.get('employment_status', '')}")
    st.write(f"**Annual Income:** ${financial_profile.get('annual_income', 0):,}")
    st.write(f"**Credit Score:** {financial_profile.get('credit_score', '')}")

# Display lender criteria data
st.header("Lender Criteria Data")
st.info("This table shows the criteria used by different lenders to evaluate loan applications.")

# Display the lender criteria dataframe
st.dataframe(lender_criteria_df, use_container_width=True)

# Allow downloading the lender criteria CSV
csv = lender_criteria_df.to_csv(index=False)
st.download_button(
    label="Download Lender Criteria CSV",
    data=csv,
    file_name="lender_criteria.csv",
    mime="text/csv"
)

# Extract client data for matching
def extract_client_data():
    # Convert credit score range to numeric value
    credit_score_map = {
        "Below 600": 580,
        "600-650": 625,
        "650-700": 675,
        "700-750": 725,
        "750+": 775,
        "Unsure": 650  # Default assumption
    }
    client_credit_score = credit_score_map[financial_profile.get('credit_score', 'Unsure')]
    
    # Calculate DTI ratio
    monthly_debt = financial_profile.get('existing_mortgage', 0) + financial_profile.get('credit_card_debt', 0)/12 + financial_profile.get('other_loans', 0)
    monthly_income = financial_profile.get('annual_income', 0) / 12
    dti_ratio = (monthly_debt / monthly_income * 100) if monthly_income > 0 else 0
    
    # Calculate LTV ratio
    ltv_ratio = (loan_requirements.get('loan_amount', 0) / property_details.get('property_value', 1) * 100) if property_details.get('property_value', 0) > 0 else 0
    
    # Get property location
    property_location = property_details.get('property_location', 'England')
    
    # Create client data dictionary
    client_data = {
        "credit_score": client_credit_score,
        "dti_ratio": dti_ratio,
        "ltv_ratio": ltv_ratio,
        "annual_income": financial_profile.get('annual_income', 0),
        "employment_years": financial_profile.get('years_employed', 0),
        "loan_amount": loan_requirements.get('loan_amount', 0),
        "bankruptcy": financial_profile.get('bankruptcy', 'No') != "No",
        "self_employed": financial_profile.get('employment_status', '') == "Self-Employed",
        "property_location": property_location
    }
    
    return client_data

# Run Model button
if st.button("Run Lender Matching Model"):
    with st.spinner("Running lender matching model..."):
        # Extract client data
        client_data = extract_client_data()
        
        # Display client data used for matching
        st.subheader("Client Data Used for Matching")
        client_data_df = pd.DataFrame({
            "Feature": list(client_data.keys()),
            "Value": list(client_data.values())
        })
        st.dataframe(client_data_df, use_container_width=True)
        
        # Match client against lender criteria
        match_results = {}
        
        # Rename first column to 'lender_name' if it's not already named that
        if 'lender_name' not in lender_criteria_df.columns and 'Lender' in lender_criteria_df.columns:
            lender_criteria_df = lender_criteria_df.rename(columns={'Lender': 'lender_name'})
        
        # Check if lender_name column exists
        if 'lender_name' not in lender_criteria_df.columns:
            # Use the first column as lender_name
            lender_criteria_df['lender_name'] = lender_criteria_df.iloc[:, 0]
        
        # Process each lender
        for _, lender_row in lender_criteria_df.iterrows():
            try:
                lender_name = lender_row["lender_name"]
                
                # Initialize match score
                match_score = 0
                max_possible_score = 0
                
                # Check location match
                location_match = False
                property_location = client_data["property_location"]
                
                # Check if the property location column exists in the lender criteria
                if property_location in lender_criteria_df.columns:
                    if lender_row.get(property_location) == 'Y':
                        location_match = True
                        match_score += 1
                else:
                    # Default to True if we can't check
                    location_match = True
                
                max_possible_score += 1
                
                # Check loan amount within range
                loan_amount_match = True
                min_loan_size_col = next((col for col in lender_criteria_df.columns if 'Minimum Loan Size' in col or 'Min Loan' in col), None)
                max_loan_size_col = next((col for col in lender_criteria_df.columns if 'Maximum Loan Size' in col or 'Max Loan' in col), None)
                
                if min_loan_size_col and max_loan_size_col:
                    min_loan = lender_row.get(min_loan_size_col)
                    max_loan = lender_row.get(max_loan_size_col)
                    
                    # Convert to numeric if possible
                    try:
                        min_loan = float(str(min_loan).replace(',', '').replace('£', ''))
                        max_loan = float(str(max_loan).replace(',', '').replace('£', ''))
                        
                        if not (pd.isna(min_loan) or pd.isna(max_loan)):
                            loan_amount_match = min_loan <= client_data["loan_amount"] <= max_loan
                            if loan_amount_match:
                                match_score += 1
                    except (ValueError, TypeError):
                        # If conversion fails, assume it matches
                        pass
                
                max_possible_score += 1
                
                # Check LTV ratio
                ltv_match = True
                max_ltv_col = next((col for col in lender_criteria_df.columns if 'Max LTV' in col), None)
                
                if max_ltv_col:
                    max_ltv = lender_row.get(max_ltv_col)
                    
                    # Convert to numeric if possible
                    try:
                        max_ltv = float(str(max_ltv).replace('%', ''))
                        
                        if not pd.isna(max_ltv):
                            ltv_match = client_data["ltv_ratio"] <= max_ltv
                            if ltv_match:
                                match_score += 1
                    except (ValueError, TypeError):
                        # If conversion fails, assume it matches
                        pass
                
                max_possible_score += 1
                
                # Calculate match percentage
                match_percentage = (match_score / max_possible_score) * 100 if max_possible_score > 0 else 0
                
                # Store match results
                match_results[lender_name] = {
                    "match_percentage": match_percentage,
                    "location_match": location_match,
                    "loan_amount_match": loan_amount_match,
                    "ltv_match": ltv_match
                }
                
            except Exception as e:
                st.error(f"Error processing lender {lender_row.get('lender_name', 'unknown')}: {str(e)}")
        
        # Sort lenders by match percentage
        sorted_lenders = sorted(match_results.items(), key=lambda x: x[1]["match_percentage"], reverse=True)
        
        # Display top matching lenders
        st.header("Top Matching Lenders")
        
        if sorted_lenders:
            # Create a DataFrame for visualization
            top_lenders_df = pd.DataFrame({
                "Lender": [lender for lender, _ in sorted_lenders],
                "Match Percentage": [match["match_percentage"] for _, match in sorted_lenders]
            })
            
            # Display top 10 lenders
            top_n = min(10, len(top_lenders_df))
            top_lenders = top_lenders_df.head(top_n)
            
            # Create bar chart
            fig = px.bar(
                top_lenders,
                x="Lender",
                y="Match Percentage",
                title=f"Top {top_n} Matching Lenders",
                color="Match Percentage",
                color_continuous_scale="Viridis",
                labels={"Match Percentage": "Match Percentage (%)"}
            )
            
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display detailed match results
            st.subheader("Detailed Match Results")
            for lender, match in sorted_lenders[:top_n]:
                with st.expander(f"{lender} - {match['match_percentage']:.1f}% Match"):
                    st.write(f"**Location Match:** {'✅' if match['location_match'] else '❌'}")
                    st.write(f"**Loan Amount Match:** {'✅' if match['loan_amount_match'] else '❌'}")
                    st.write(f"**LTV Match:** {'✅' if match['ltv_match'] else '❌'}")
                    
                    # Get lender details
                    lender_details = lender_criteria_df[lender_criteria_df['lender_name'] == lender]
                    if not lender_details.empty:
                        st.write("**Lender Details:**")
                        for col in lender_details.columns:
                            if col != 'lender_name' and not pd.isna(lender_details.iloc[0][col]):
                                st.write(f"- {col}: {lender_details.iloc[0][col]}")
        else:
            st.warning("No matching lenders found. Please adjust your criteria.")
        
        # Feature importance analysis
        st.header("Feature Importance Analysis")
        st.info("This analysis shows which factors were most important in determining lender matches.")
        
        # Create a simple feature importance visualization
        features = ["Location", "Loan Amount", "LTV Ratio"]
        importance = [
            sum(1 for match in match_results.values() if match["location_match"]),
            sum(1 for match in match_results.values() if match["loan_amount_match"]),
            sum(1 for match in match_results.values() if match["ltv_match"])
        ]
        
        # Normalize importance
        total = sum(importance)
        normalized_importance = [i/total*100 if total > 0 else 0 for i in importance]
        
        # Create feature importance chart
        fig = px.bar(
            x=features,
            y=normalized_importance,
            title="Feature Importance in Lender Matching",
            labels={"x": "Feature", "y": "Importance (%)"},
            color=normalized_importance,
            color_continuous_scale="Viridis"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Save results to session state
        st.session_state.lender_matching['matched_lenders'] = sorted_lenders
        
        st.success("Lender matching completed successfully!")
        st.balloons() 
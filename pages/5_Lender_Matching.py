import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os
from datetime import datetime

st.set_page_config(
    page_title="Lender Matching",
    page_icon="🎯",
    layout="wide"
)

st.title("Step 5: Lender Matching")
st.markdown("Match the transcoded client profile to lenders with probability of success")

# Check if previous steps are completed
if 'verified_profile' not in st.session_state:
    st.warning("Please complete Step 4: Broker Verification first.")
    st.stop()

# Initialize session state for lender matching
if 'lender_matching' not in st.session_state:
    st.session_state.lender_matching = {
        'matched_lenders': [],
        'research_matrix_results': {},
        'unstructured_criteria_results': {},
        'final_probabilities': {}
    }

# Get verified client profile
verified_profile = st.session_state.verified_profile

# Display client profile summary
st.header("Client Profile Summary")
client_col1, client_col2 = st.columns(2)

with client_col1:
    client_profile = verified_profile['client_profile']
    st.subheader("Client Information")
    st.write(f"**Name:** {client_profile['first_name']} {client_profile['last_name']}")
    st.write(f"**Email:** {client_profile['email']}")
    st.write(f"**Phone:** {client_profile['phone']}")
    
    loan_requirements = verified_profile['loan_requirements']
    st.subheader("Loan Requirements")
    st.write(f"**Loan Purpose:** {loan_requirements['loan_purpose']}")
    st.write(f"**Loan Amount:** ${loan_requirements['loan_amount']:,}")
    st.write(f"**Down Payment:** ${loan_requirements['down_payment']:,}")
    st.write(f"**Preferred Term:** {loan_requirements['loan_term_preference']}")

with client_col2:
    property_details = verified_profile['property_details']
    st.subheader("Property Details")
    st.write(f"**Property Type:** {property_details['property_type']}")
    st.write(f"**Property Value:** ${property_details['property_value']:,}")
    st.write(f"**Property Use:** {property_details['property_use']}")
    
    financial_profile = verified_profile['financial_profile']
    st.subheader("Financial Profile")
    st.write(f"**Employment:** {financial_profile['employment_status']}")
    st.write(f"**Annual Income:** ${financial_profile['annual_income']:,}")
    st.write(f"**Credit Score:** {financial_profile['credit_score']}")

# Research Matrix Matching
st.header("Research Matrix Matching")
st.info("This section matches the client profile against structured lender criteria in the research matrix.")

# Create a function to generate a research matrix with lender criteria
def generate_research_matrix():
    # In a real implementation, this would be loaded from a database
    lenders = [
        "Arose Finance Prime",
        "Arose Finance Standard",
        "Arose Finance Flexible",
        "Partner Bank A",
        "Partner Bank B",
        "Partner Credit Union",
        "Specialist Lender X",
        "Specialist Lender Y",
        "Specialist Lender Z"
    ]
    
    # Define criteria columns
    criteria = [
        "min_credit_score",
        "max_dti",
        "max_ltv",
        "min_income",
        "min_employment_years",
        "max_loan_amount",
        "property_types",
        "loan_purposes",
        "bankruptcy_allowed",
        "self_employed_allowed"
    ]
    
    # Create empty dataframe
    matrix = pd.DataFrame(index=lenders, columns=criteria)
    
    # Fill with sample data (in a real implementation, this would be actual lender criteria)
    matrix.loc["Arose Finance Prime"] = [720, 36, 80, 75000, 2, 1000000, ["Single Family Home", "Condominium"], ["Home Purchase", "Refinance"], False, True]
    matrix.loc["Arose Finance Standard"] = [680, 43, 90, 50000, 1, 750000, ["Single Family Home", "Condominium", "Townhouse"], ["Home Purchase", "Refinance", "Home Improvement"], False, True]
    matrix.loc["Arose Finance Flexible"] = [620, 50, 95, 35000, 0.5, 500000, ["Single Family Home", "Condominium", "Townhouse", "Multi-Family Home"], ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation"], True, True]
    matrix.loc["Partner Bank A"] = [700, 40, 85, 60000, 2, 850000, ["Single Family Home", "Condominium"], ["Home Purchase", "Refinance"], False, False]
    matrix.loc["Partner Bank B"] = [660, 45, 90, 45000, 1, 600000, ["Single Family Home", "Condominium", "Townhouse"], ["Home Purchase", "Refinance", "Home Improvement"], False, True]
    matrix.loc["Partner Credit Union"] = [640, 48, 95, 40000, 0.5, 450000, ["Single Family Home", "Condominium", "Townhouse"], ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation"], True, True]
    matrix.loc["Specialist Lender X"] = [580, 55, 90, 30000, 0, 350000, ["Single Family Home", "Condominium", "Townhouse", "Multi-Family Home"], ["Home Purchase", "Refinance", "Debt Consolidation"], True, True]
    matrix.loc["Specialist Lender Y"] = [700, 43, 70, 100000, 3, 2000000, ["Single Family Home", "Condominium", "Commercial Property"], ["Home Purchase", "Refinance", "Business"], False, True]
    matrix.loc["Specialist Lender Z"] = [620, 50, 100, 35000, 0.5, 400000, ["Single Family Home", "Condominium", "Townhouse", "Land"], ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation"], True, True]
    
    return matrix

# Generate research matrix
research_matrix = generate_research_matrix()

# Display research matrix
with st.expander("View Research Matrix"):
    st.dataframe(research_matrix)

# Extract client data for matching
client_data = {
    "credit_score": financial_profile['credit_score'],
    "annual_income": financial_profile['annual_income'],
    "employment_years": financial_profile['years_employed'],
    "loan_amount": loan_requirements['loan_amount'],
    "property_type": property_details['property_type'],
    "loan_purpose": loan_requirements['loan_purpose'],
    "bankruptcy": financial_profile['bankruptcy'] != "No",
    "self_employed": financial_profile['employment_status'] == "Self-Employed"
}

# Convert credit score range to numeric value
credit_score_map = {
    "Below 600": 580,
    "600-650": 625,
    "650-700": 675,
    "700-750": 725,
    "750+": 775,
    "Unsure": 650  # Default assumption
}
client_credit_score = credit_score_map[client_data["credit_score"]]

# Calculate DTI ratio
monthly_debt = financial_profile['existing_mortgage'] + financial_profile['credit_card_debt']/12 + financial_profile['other_loans']
monthly_income = financial_profile['annual_income'] / 12
dti_ratio = (monthly_debt / monthly_income * 100) if monthly_income > 0 else 0

# Calculate LTV ratio
ltv_ratio = (loan_requirements['loan_amount'] / property_details['property_value'] * 100) if property_details['property_value'] > 0 else 0

# Match client against research matrix
match_results = {}
for lender in research_matrix.index:
    criteria = research_matrix.loc[lender]
    
    # Check each criterion
    credit_score_match = client_credit_score >= criteria["min_credit_score"]
    dti_match = dti_ratio <= criteria["max_dti"]
    ltv_match = ltv_ratio <= criteria["max_ltv"]
    income_match = client_data["annual_income"] >= criteria["min_income"]
    employment_match = client_data["employment_years"] >= criteria["min_employment_years"]
    loan_amount_match = client_data["loan_amount"] <= criteria["max_loan_amount"]
    property_type_match = client_data["property_type"] in criteria["property_types"]
    loan_purpose_match = client_data["loan_purpose"] in criteria["loan_purposes"]
    bankruptcy_match = not client_data["bankruptcy"] or criteria["bankruptcy_allowed"]
    self_employed_match = not client_data["self_employed"] or criteria["self_employed_allowed"]
    
    # Calculate match percentage
    criteria_results = [
        credit_score_match,
        dti_match,
        ltv_match,
        income_match,
        employment_match,
        loan_amount_match,
        property_type_match,
        loan_purpose_match,
        bankruptcy_match,
        self_employed_match
    ]
    
    match_percentage = sum(criteria_results) / len(criteria_results) * 100
    
    # Store results
    match_results[lender] = {
        "match_percentage": match_percentage,
        "criteria_results": {
            "Credit Score": credit_score_match,
            "DTI Ratio": dti_match,
            "LTV Ratio": ltv_match,
            "Income": income_match,
            "Employment History": employment_match,
            "Loan Amount": loan_amount_match,
            "Property Type": property_type_match,
            "Loan Purpose": loan_purpose_match,
            "Bankruptcy": bankruptcy_match,
            "Self-Employed": self_employed_match
        }
    }

# Display match results
st.subheader("Matrix Matching Results")
match_data = []
for lender, result in match_results.items():
    match_data.append({
        "Lender": lender,
        "Match Percentage": f"{result['match_percentage']:.1f}%",
        "Match Score": result['match_percentage']
    })

match_df = pd.DataFrame(match_data)
match_df = match_df.sort_values("Match Score", ascending=False)

# Display as bar chart
fig = px.bar(
    match_df,
    x="Lender",
    y="Match Score",
    title="Lender Match Percentages (Research Matrix)",
    labels={"Match Score": "Match Percentage (%)"},
    color="Match Score",
    color_continuous_scale="RdYlGn"
)
st.plotly_chart(fig, use_container_width=True)

# Unstructured Criteria Matching
st.header("Unstructured Criteria Enrichment")
st.info("This section enriches the matching with unstructured lender criteria transcriptions.")

# Function to simulate unstructured criteria matching
def unstructured_criteria_matching(client_data, match_results):
    # In a real implementation, this would use NLP to match client data against unstructured text
    # For this demo, we'll simulate adjustments to the match percentages
    
    enriched_results = match_results.copy()
    
    # Simulate adjustments based on unstructured criteria
    for lender in enriched_results:
        # Random adjustment between -10% and +10%
        adjustment = np.random.uniform(-10, 10)
        
        # Apply some logic-based adjustments
        if "Specialist" in lender and client_data["credit_score"] in ["Below 600", "600-650"]:
            adjustment += 5  # Specialist lenders may be more flexible with lower credit scores
        
        if "Flexible" in lender and client_data["bankruptcy"]:
            adjustment += 7  # Flexible programs may be more accommodating of bankruptcy
        
        if "Prime" in lender and client_data["credit_score"] in ["750+"]:
            adjustment += 5  # Prime lenders prefer excellent credit
        
        # Apply adjustment
        new_percentage = enriched_results[lender]["match_percentage"] + adjustment
        
        # Ensure percentage is between 0 and 100
        new_percentage = max(0, min(100, new_percentage))
        
        enriched_results[lender]["match_percentage"] = new_percentage
        enriched_results[lender]["adjustment"] = adjustment
    
    return enriched_results

# Apply unstructured criteria matching
enriched_results = unstructured_criteria_matching(client_data, match_results)

# Display enriched results
st.subheader("Enriched Matching Results")
enriched_data = []
for lender, result in enriched_results.items():
    enriched_data.append({
        "Lender": lender,
        "Original Match": f"{match_results[lender]['match_percentage']:.1f}%",
        "Adjustment": f"{result['adjustment']:+.1f}%",
        "Final Match": f"{result['match_percentage']:.1f}%",
        "Final Score": result['match_percentage']
    })

enriched_df = pd.DataFrame(enriched_data)
enriched_df = enriched_df.sort_values("Final Score", ascending=False)

st.dataframe(enriched_df, use_container_width=True)

# Display as bar chart
fig = px.bar(
    enriched_df,
    x="Lender",
    y="Final Score",
    title="Final Lender Match Percentages",
    labels={"Final Score": "Match Percentage (%)"},
    color="Final Score",
    color_continuous_scale="RdYlGn"
)
st.plotly_chart(fig, use_container_width=True)

# Final Lender Recommendations
st.header("Final Lender Recommendations")

# Get top 3 lenders
top_lenders = enriched_df.nlargest(3, "Final Score")

# Display top lenders
st.subheader("Top Recommended Lenders")
for i, (_, lender) in enumerate(top_lenders.iterrows()):
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.metric(f"#{i+1}", lender["Lender"], f"{lender['Final Score']:.1f}%")
    
    with col2:
        # Display lender details
        if "Arose Finance" in lender["Lender"]:
            if "Prime" in lender["Lender"]:
                st.write("**Description:** Premium loan program with the best rates for well-qualified borrowers.")
            elif "Standard" in lender["Lender"]:
                st.write("**Description:** Standard loan program with competitive rates for qualified borrowers.")
            elif "Flexible" in lender["Lender"]:
                st.write("**Description:** Flexible loan program designed for borrowers with less-than-perfect credit or unique situations.")
        elif "Partner Bank" in lender["Lender"]:
            if "A" in lender["Lender"]:
                st.write("**Description:** Partner Bank A offers competitive rates with flexible terms for well-qualified borrowers.")
            elif "B" in lender["Lender"]:
                st.write("**Description:** Partner Bank B specializes in loans for first-time homebuyers and those with moderate income.")
        elif "Partner Credit Union" in lender["Lender"]:
            st.write("**Description:** Partner Credit Union offers member-focused loans with personalized service and competitive rates.")
        elif "Specialist Lender" in lender["Lender"]:
            if "X" in lender["Lender"]:
                st.write("**Description:** Specialist Lender X focuses on borrowers with credit challenges and offers flexible qualification criteria.")
            elif "Y" in lender["Lender"]:
                st.write("**Description:** Specialist Lender Y specializes in jumbo loans and high-value properties with excellent terms for qualified borrowers.")
            elif "Z" in lender["Lender"]:
                st.write("**Description:** Specialist Lender Z offers 100% financing options and specialized programs for unique property types.")
        
        # Display criteria that weren't met
        failed_criteria = [
            criterion for criterion, result in match_results[lender["Lender"]]["criteria_results"].items() if not result
        ]
        
        if failed_criteria:
            st.warning(f"**Potential Issues:** This lender's criteria for {', '.join(failed_criteria)} were not fully met.")
        else:
            st.success("**Perfect Match:** All of this lender's criteria were met!")

# Save results
if st.button("Save Lender Matching Results"):
    # Save to session state
    st.session_state.lender_matching = {
        'matched_lenders': enriched_df.to_dict('records'),
        'research_matrix_results': match_results,
        'unstructured_criteria_results': enriched_results,
        'final_probabilities': top_lenders.to_dict('records')
    }
    
    st.success("Lender matching results saved successfully!")
    
    # Display output
    st.subheader("Output Generated")
    st.markdown("✅ List of viable lenders with probability of application success")
    
    st.balloons() 
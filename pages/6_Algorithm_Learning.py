import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Algorithm Learning",
    page_icon="🧠",
    layout="wide"
)

st.title("Step 6: Algorithm Self-Education")
st.markdown("Algorithm self-educates based on loan outcomes and feedback")

# Check if previous steps are completed
if 'lender_matching' not in st.session_state:
    st.warning("Please complete Step 5: Lender Matching first.")
    st.stop()

# Initialize session state for algorithm learning
if 'algorithm_learning' not in st.session_state:
    st.session_state.algorithm_learning = {
        'historical_outcomes': [],
        'learning_events': [],
        'algorithm_updates': []
    }

# Load historical data (in a real implementation, this would come from a database)
if 'historical_data' not in st.session_state:
    # Create sample historical data
    historical_data = []
    np.random.seed(42)  # For reproducibility
    
    # Generate 50 sample loan applications with outcomes
    for i in range(50):
        # Generate random client profile
        credit_scores = ["Below 600", "600-650", "650-700", "700-750", "750+"]
        credit_score = np.random.choice(credit_scores, p=[0.1, 0.2, 0.3, 0.25, 0.15])
        
        income_levels = [35000, 50000, 75000, 100000, 150000, 200000]
        income = np.random.choice(income_levels, p=[0.15, 0.25, 0.3, 0.15, 0.1, 0.05])
        
        loan_purposes = ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation"]
        loan_purpose = np.random.choice(loan_purposes)
        
        property_types = ["Single Family Home", "Condominium", "Townhouse", "Multi-Family Home"]
        property_type = np.random.choice(property_types, p=[0.6, 0.2, 0.15, 0.05])
        
        # Generate loan details
        loan_amount = np.random.randint(100000, 500000)
        ltv_ratio = np.random.uniform(60, 100)
        dti_ratio = np.random.uniform(20, 55)
        
        # Selected lender
        lenders = [
            "Arose Finance Prime", 
            "Arose Finance Standard", 
            "Arose Finance Flexible",
            "Partner Bank A",
            "Partner Bank B",
            "Partner Credit Union"
        ]
        selected_lender = np.random.choice(lenders)
        
        # Determine outcome based on profile
        # Higher credit scores, lower LTV/DTI ratios increase success probability
        success_prob = 0.5
        
        if credit_score == "750+":
            success_prob += 0.3
        elif credit_score == "700-750":
            success_prob += 0.2
        elif credit_score == "650-700":
            success_prob += 0.1
        elif credit_score == "600-650":
            success_prob -= 0.1
        elif credit_score == "Below 600":
            success_prob -= 0.3
            
        if ltv_ratio > 90:
            success_prob -= 0.2
        elif ltv_ratio > 80:
            success_prob -= 0.1
            
        if dti_ratio > 45:
            success_prob -= 0.2
        elif dti_ratio > 36:
            success_prob -= 0.1
            
        if income > 100000:
            success_prob += 0.1
            
        # Cap probability between 0.1 and 0.9
        success_prob = max(0.1, min(0.9, success_prob))
        
        # Determine outcome
        outcome = np.random.choice(["Approved", "Declined"], p=[success_prob, 1-success_prob])
        
        # If approved, determine if loan completed
        completed = "N/A"
        completion_reason = "N/A"
        
        if outcome == "Approved":
            completed = np.random.choice(["Yes", "No"], p=[0.8, 0.2])
            
            if completed == "No":
                reasons = [
                    "Client found better rate elsewhere",
                    "Property appraisal came in too low",
                    "Client's financial situation changed",
                    "Documentation issues",
                    "Client withdrew application"
                ]
                completion_reason = np.random.choice(reasons)
        
        # Add to historical data
        historical_data.append({
            "Application ID": f"LOAN-{2023000 + i}",
            "Application Date": (datetime.now() - timedelta(days=np.random.randint(30, 365))).strftime("%Y-%m-%d"),
            "Credit Score": credit_score,
            "Annual Income": income,
            "Loan Purpose": loan_purpose,
            "Property Type": property_type,
            "Loan Amount": loan_amount,
            "LTV Ratio": ltv_ratio,
            "DTI Ratio": dti_ratio,
            "Selected Lender": selected_lender,
            "Outcome": outcome,
            "Loan Completed": completed,
            "Reason (if not completed)": completion_reason
        })
    
    st.session_state.historical_data = historical_data

# Display historical data
st.header("Historical Loan Outcomes")
st.info("The algorithm learns from historical loan outcomes to improve future matching.")

# Convert to DataFrame for easier manipulation
historical_df = pd.DataFrame(st.session_state.historical_data)

# Display summary statistics
col1, col2, col3 = st.columns(3)

with col1:
    total_applications = len(historical_df)
    approved_applications = len(historical_df[historical_df["Outcome"] == "Approved"])
    approval_rate = approved_applications / total_applications * 100
    
    st.metric("Total Applications", total_applications)
    st.metric("Approval Rate", f"{approval_rate:.1f}%")

with col2:
    completed_loans = len(historical_df[(historical_df["Outcome"] == "Approved") & (historical_df["Loan Completed"] == "Yes")])
    completion_rate = completed_loans / approved_applications * 100 if approved_applications > 0 else 0
    
    st.metric("Approved Applications", approved_applications)
    st.metric("Completion Rate", f"{completion_rate:.1f}%")

with col3:
    fallout_loans = len(historical_df[(historical_df["Outcome"] == "Approved") & (historical_df["Loan Completed"] == "No")])
    fallout_rate = fallout_loans / approved_applications * 100 if approved_applications > 0 else 0
    
    st.metric("Incomplete Loans", fallout_loans)
    st.metric("Fallout Rate", f"{fallout_rate:.1f}%")

# Display historical data table
with st.expander("View Historical Data"):
    st.dataframe(historical_df, use_container_width=True)

# Learning from successful applications
st.header("Learning from Successful Applications")
st.info("When applications are successful (loan completes), the algorithm is reinforced by the success.")

# Filter for successful applications
successful_df = historical_df[(historical_df["Outcome"] == "Approved") & (historical_df["Loan Completed"] == "Yes")]

# Display success patterns
st.subheader("Success Patterns")

# Credit score distribution for successful loans
fig = px.histogram(
    successful_df,
    x="Credit Score",
    title="Credit Score Distribution for Successful Loans",
    category_orders={"Credit Score": ["Below 600", "600-650", "650-700", "700-750", "750+"]},
    color="Credit Score",
    color_discrete_sequence=px.colors.sequential.Greens
)
st.plotly_chart(fig, use_container_width=True)

# Success by lender
success_by_lender = successful_df.groupby("Selected Lender").size().reset_index(name="Successful Loans")
fig = px.bar(
    success_by_lender,
    x="Selected Lender",
    y="Successful Loans",
    title="Successful Loans by Lender",
    color="Successful Loans",
    color_continuous_scale="Greens"
)
st.plotly_chart(fig, use_container_width=True)

# Learning from unsuccessful applications
st.header("Learning from Unsuccessful Applications")
st.info("When applications are unsuccessful (loan does not complete), the algorithm is educated by the experience.")

# Filter for unsuccessful applications
unsuccessful_df = historical_df[(historical_df["Outcome"] == "Approved") & (historical_df["Loan Completed"] == "No")]

# Display failure patterns
st.subheader("Failure Patterns")

# Reasons for incompletion
reasons_count = unsuccessful_df["Reason (if not completed)"].value_counts().reset_index()
reasons_count.columns = ["Reason", "Count"]

fig = px.pie(
    reasons_count,
    values="Count",
    names="Reason",
    title="Reasons for Loan Non-Completion"
)
st.plotly_chart(fig, use_container_width=True)

# Failure by lender
failure_by_lender = unsuccessful_df.groupby("Selected Lender").size().reset_index(name="Failed Loans")
fig = px.bar(
    failure_by_lender,
    x="Selected Lender",
    y="Failed Loans",
    title="Failed Loans by Lender",
    color="Failed Loans",
    color_continuous_scale="Reds"
)
st.plotly_chart(fig, use_container_width=True)

# Algorithm Learning Simulation
st.header("Algorithm Learning Simulation")
st.info("This section demonstrates how the algorithm updates its matching criteria based on outcomes.")

# Create a new loan application
st.subheader("New Loan Application")
st.write("Enter details for a new loan application to see how the algorithm would apply its learning:")

col1, col2 = st.columns(2)

with col1:
    new_credit_score = st.selectbox(
        "Credit Score",
        ["Below 600", "600-650", "650-700", "700-750", "750+"],
        index=2
    )
    
    new_income = st.number_input(
        "Annual Income ($)",
        min_value=25000,
        max_value=500000,
        value=75000,
        step=5000
    )
    
    new_loan_purpose = st.selectbox(
        "Loan Purpose",
        ["Home Purchase", "Refinance", "Home Improvement", "Debt Consolidation"]
    )

with col2:
    new_property_type = st.selectbox(
        "Property Type",
        ["Single Family Home", "Condominium", "Townhouse", "Multi-Family Home"]
    )
    
    new_loan_amount = st.number_input(
        "Loan Amount ($)",
        min_value=50000,
        max_value=1000000,
        value=250000,
        step=10000
    )
    
    new_ltv = st.slider(
        "LTV Ratio (%)",
        min_value=50,
        max_value=100,
        value=80
    )
    
    new_dti = st.slider(
        "DTI Ratio (%)",
        min_value=20,
        max_value=60,
        value=36
    )

# Simulate algorithm learning
if st.button("Simulate Algorithm Learning"):
    # Create a function to calculate base match percentages
    def calculate_base_match(client_data, lenders):
        match_results = {}
        
        for lender in lenders:
            # Simple matching logic
            score = 50  # Start with neutral score
            
            # Credit score factor
            if client_data["credit_score"] == "750+":
                score += 20
            elif client_data["credit_score"] == "700-750":
                score += 15
            elif client_data["credit_score"] == "650-700":
                score += 10
            elif client_data["credit_score"] == "600-650":
                score -= 5
            elif client_data["credit_score"] == "Below 600":
                score -= 15
            
            # LTV factor
            if client_data["ltv"] <= 80:
                score += 10
            elif client_data["ltv"] <= 90:
                score += 5
            else:
                score -= 10
            
            # DTI factor
            if client_data["dti"] <= 36:
                score += 10
            elif client_data["dti"] <= 43:
                score += 5
            else:
                score -= 10
            
            # Income factor
            if client_data["income"] >= 100000:
                score += 10
            elif client_data["income"] >= 75000:
                score += 5
            
            # Lender-specific adjustments
            if "Prime" in lender and client_data["credit_score"] in ["700-750", "750+"]:
                score += 15
            elif "Flexible" in lender and client_data["credit_score"] in ["600-650", "Below 600"]:
                score += 10
            elif "Credit Union" in lender and client_data["loan_purpose"] == "Home Purchase":
                score += 5
            
            # Ensure score is between 0 and 100
            score = max(0, min(100, score))
            
            match_results[lender] = score
        
        return match_results
    
    # Create a function to apply learning from historical data
    def apply_learning(base_matches, client_data, historical_data):
        learned_matches = base_matches.copy()
        learning_events = []
        
        # Convert historical data to DataFrame if it's not already
        if not isinstance(historical_data, pd.DataFrame):
            historical_data = pd.DataFrame(historical_data)
        
        # Apply learning from successful loans
        successful_loans = historical_data[(historical_data["Outcome"] == "Approved") & (historical_data["Loan Completed"] == "Yes")]
        
        # For each lender, analyze success patterns
        for lender in learned_matches.keys():
            lender_successes = successful_loans[successful_loans["Selected Lender"] == lender]
            
            if len(lender_successes) > 0:
                # Credit score learning
                credit_success = lender_successes["Credit Score"].value_counts(normalize=True)
                if client_data["credit_score"] in credit_success and credit_success[client_data["credit_score"]] > 0.2:
                    adjustment = 5
                    learned_matches[lender] += adjustment
                    learning_events.append(f"Reinforced {lender} match by +{adjustment} based on successful credit score pattern")
                
                # LTV learning
                avg_ltv = lender_successes["LTV Ratio"].mean()
                if abs(client_data["ltv"] - avg_ltv) < 10:
                    adjustment = 3
                    learned_matches[lender] += adjustment
                    learning_events.append(f"Reinforced {lender} match by +{adjustment} based on successful LTV pattern")
                
                # Loan purpose learning
                purpose_success = lender_successes["Loan Purpose"].value_counts(normalize=True)
                if client_data["loan_purpose"] in purpose_success and purpose_success[client_data["loan_purpose"]] > 0.3:
                    adjustment = 4
                    learned_matches[lender] += adjustment
                    learning_events.append(f"Reinforced {lender} match by +{adjustment} based on successful loan purpose pattern")
        
        # Apply learning from unsuccessful loans
        unsuccessful_loans = historical_data[(historical_data["Outcome"] == "Approved") & (historical_data["Loan Completed"] == "No")]
        
        # For each lender, analyze failure patterns
        for lender in learned_matches.keys():
            lender_failures = unsuccessful_loans[unsuccessful_loans["Selected Lender"] == lender]
            
            if len(lender_failures) > 0:
                # Credit score learning
                credit_failure = lender_failures["Credit Score"].value_counts(normalize=True)
                if client_data["credit_score"] in credit_failure and credit_failure[client_data["credit_score"]] > 0.2:
                    adjustment = -5
                    learned_matches[lender] += adjustment
                    learning_events.append(f"Adjusted {lender} match by {adjustment} based on unsuccessful credit score pattern")
                
                # LTV learning
                avg_failed_ltv = lender_failures["LTV Ratio"].mean()
                if abs(client_data["ltv"] - avg_failed_ltv) < 5:
                    adjustment = -3
                    learned_matches[lender] += adjustment
                    learning_events.append(f"Adjusted {lender} match by {adjustment} based on unsuccessful LTV pattern")
                
                # Reason analysis
                if "documentation issues" in lender_failures["Reason (if not completed)"].str.lower().values:
                    adjustment = -2
                    learned_matches[lender] += adjustment
                    learning_events.append(f"Adjusted {lender} match by {adjustment} due to historical documentation issues")
        
        # Ensure all scores are between 0 and 100
        for lender in learned_matches:
            learned_matches[lender] = max(0, min(100, learned_matches[lender]))
        
        return learned_matches, learning_events
    
    # Create client data dictionary
    client_data = {
        "credit_score": new_credit_score,
        "income": new_income,
        "loan_purpose": new_loan_purpose,
        "property_type": new_property_type,
        "loan_amount": new_loan_amount,
        "ltv": new_ltv,
        "dti": new_dti
    }
    
    # List of lenders
    lenders = [
        "Arose Finance Prime", 
        "Arose Finance Standard", 
        "Arose Finance Flexible",
        "Partner Bank A",
        "Partner Bank B",
        "Partner Credit Union"
    ]
    
    # Calculate base match percentages
    base_matches = calculate_base_match(client_data, lenders)
    
    # Apply learning from historical data
    learned_matches, learning_events = apply_learning(base_matches, client_data, st.session_state.historical_data)
    
    # Display results
    st.subheader("Algorithm Learning Results")
    
    # Create comparison dataframe
    comparison_data = []
    for lender in base_matches:
        comparison_data.append({
            "Lender": lender,
            "Base Match": base_matches[lender],
            "Learned Match": learned_matches[lender],
            "Adjustment": learned_matches[lender] - base_matches[lender]
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Display as bar chart
    fig = px.bar(
        comparison_df,
        x="Lender",
        y=["Base Match", "Learned Match"],
        title="Impact of Algorithm Learning on Match Percentages",
        barmode="group",
        labels={"value": "Match Percentage (%)"}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Display comparison table
    st.dataframe(comparison_df, use_container_width=True)
    
    # Display learning events
    st.subheader("Learning Events")
    for event in learning_events:
        st.write(f"- {event}")
    
    # Save to session state
    st.session_state.algorithm_learning = {
        'historical_outcomes': st.session_state.historical_data,
        'learning_events': learning_events,
        'algorithm_updates': comparison_data
    }
    
    st.success("Algorithm learning simulation completed successfully!")
    
    # Display output
    st.subheader("Output Generated")
    st.markdown("✅ Updated matching algorithm based on historical outcomes")
    
    st.balloons() 
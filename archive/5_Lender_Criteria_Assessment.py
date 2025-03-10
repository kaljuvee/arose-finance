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
    page_title="Lender Criteria Assessment",
    page_icon="🎯",
    layout="wide"
)

st.title("Step 5: Lender Criteria Assessment")
st.markdown("Determine if the application meets lender requirements")

# Initialize session state for lender criteria assessment
if 'lender_criteria' not in st.session_state:
    st.session_state.lender_criteria = {
        'lender_selection': None,
        'criteria_met': {},
        'overall_assessment': None,
        'recommendation': None,
        'model_confidence': None
    }

# Check if we have financial analysis data
has_financial_data = 'financial_analysis' in st.session_state and st.session_state.financial_analysis.get('risk_assessment')

# Check if we have credit data
has_credit_data = 'credit_data' in st.session_state and st.session_state.credit_data.get('credit_score') is not None

# Check if we have application data
has_application_data = 'application_data' in st.session_state and st.session_state.application_data.get('loan_info')

if not has_financial_data or not has_credit_data or not has_application_data:
    st.warning("Complete previous steps before proceeding with lender criteria assessment.")
    if not has_financial_data:
        st.error("Missing financial analysis data. Please complete the Financial Analysis step.")
    if not has_credit_data:
        st.error("Missing credit data. Please complete the Credit Bureau Integration step.")
    if not has_application_data:
        st.error("Missing application data. Please complete the Application Intake step.")
else:
    # Get data from session state
    financial_analysis = st.session_state.financial_analysis
    credit_data = st.session_state.credit_data
    application_data = st.session_state.application_data
    
    # Lender Selection
    st.header("Lender Selection")
    
    lender_options = [
        "Arose Finance Prime",
        "Arose Finance Standard",
        "Arose Finance Flexible",
        "Partner Bank A",
        "Partner Bank B",
        "Partner Credit Union"
    ]
    
    selected_lender = st.selectbox(
        "Select Lender Program",
        lender_options,
        index=0,
        key="selected_lender"
    )
    
    # Display lender criteria based on selection
    st.subheader(f"{selected_lender} Criteria")
    
    # Define lender criteria (these would typically come from a database)
    lender_criteria = {
        "Arose Finance Prime": {
            "min_credit_score": 720,
            "max_dti": 36,
            "max_ltv": 80,
            "min_income": 75000,
            "min_employment_years": 2,
            "max_loan_amount": 1000000,
            "description": "Our premium loan program with the best rates for well-qualified borrowers."
        },
        "Arose Finance Standard": {
            "min_credit_score": 680,
            "max_dti": 43,
            "max_ltv": 90,
            "min_income": 50000,
            "min_employment_years": 1,
            "max_loan_amount": 750000,
            "description": "Our standard loan program with competitive rates for qualified borrowers."
        },
        "Arose Finance Flexible": {
            "min_credit_score": 620,
            "max_dti": 50,
            "max_ltv": 95,
            "min_income": 35000,
            "min_employment_years": 0.5,
            "max_loan_amount": 500000,
            "description": "Our flexible loan program designed for borrowers with less-than-perfect credit or unique situations."
        },
        "Partner Bank A": {
            "min_credit_score": 700,
            "max_dti": 40,
            "max_ltv": 85,
            "min_income": 60000,
            "min_employment_years": 2,
            "max_loan_amount": 850000,
            "description": "Partner Bank A offers competitive rates with flexible terms for well-qualified borrowers."
        },
        "Partner Bank B": {
            "min_credit_score": 660,
            "max_dti": 45,
            "max_ltv": 90,
            "min_income": 45000,
            "min_employment_years": 1,
            "max_loan_amount": 600000,
            "description": "Partner Bank B specializes in loans for first-time homebuyers and those with moderate income."
        },
        "Partner Credit Union": {
            "min_credit_score": 640,
            "max_dti": 48,
            "max_ltv": 95,
            "min_income": 40000,
            "min_employment_years": 0.5,
            "max_loan_amount": 450000,
            "description": "Partner Credit Union offers member-focused loans with personalized service and competitive rates."
        }
    }
    
    # Display selected lender criteria
    st.info(lender_criteria[selected_lender]["description"])
    
    criteria_col1, criteria_col2 = st.columns(2)
    
    with criteria_col1:
        st.write("**Required Criteria:**")
        st.write(f"- Minimum Credit Score: {lender_criteria[selected_lender]['min_credit_score']}")
        st.write(f"- Maximum DTI Ratio: {lender_criteria[selected_lender]['max_dti']}%")
        st.write(f"- Maximum LTV Ratio: {lender_criteria[selected_lender]['max_ltv']}%")
    
    with criteria_col2:
        st.write("**Additional Requirements:**")
        st.write(f"- Minimum Annual Income: ${lender_criteria[selected_lender]['min_income']:,}")
        st.write(f"- Minimum Employment History: {lender_criteria[selected_lender]['min_employment_years']} years")
        st.write(f"- Maximum Loan Amount: ${lender_criteria[selected_lender]['max_loan_amount']:,}")
    
    # Criteria Assessment
    st.header("Criteria Assessment")
    
    # Get borrower data
    credit_score = credit_data['credit_score']
    dti_ratio = financial_analysis['ratios']['dti_ratio']
    ltv_ratio = financial_analysis['ratios']['ltv_ratio']
    annual_income = financial_analysis['income_analysis']['monthly_income'] * 12
    employment_years = application_data['employment_info'].get('years_employed', 0)
    loan_amount = application_data['loan_info'].get('loan_amount', 0)
    
    # Create assessment table
    assessment_data = {
        "Criteria": [
            "Credit Score",
            "DTI Ratio",
            "LTV Ratio",
            "Annual Income",
            "Employment History",
            "Loan Amount"
        ],
        "Requirement": [
            f">= {lender_criteria[selected_lender]['min_credit_score']}",
            f"<= {lender_criteria[selected_lender]['max_dti']}%",
            f"<= {lender_criteria[selected_lender]['max_ltv']}%",
            f">= ${lender_criteria[selected_lender]['min_income']:,}",
            f">= {lender_criteria[selected_lender]['min_employment_years']} years",
            f"<= ${lender_criteria[selected_lender]['max_loan_amount']:,}"
        ],
        "Borrower": [
            f"{credit_score}",
            f"{dti_ratio:.2f}%",
            f"{ltv_ratio:.2f}%",
            f"${annual_income:,.2f}",
            f"{employment_years} years" if employment_years else "Unknown",
            f"${loan_amount:,.2f}"
        ],
        "Status": [
            "✅ Met" if credit_score >= lender_criteria[selected_lender]['min_credit_score'] else "❌ Not Met",
            "✅ Met" if dti_ratio <= lender_criteria[selected_lender]['max_dti'] else "❌ Not Met",
            "✅ Met" if ltv_ratio <= lender_criteria[selected_lender]['max_ltv'] else "❌ Not Met",
            "✅ Met" if annual_income >= lender_criteria[selected_lender]['min_income'] else "❌ Not Met",
            "✅ Met" if employment_years and employment_years >= lender_criteria[selected_lender]['min_employment_years'] else "❌ Not Met",
            "✅ Met" if loan_amount <= lender_criteria[selected_lender]['max_loan_amount'] else "❌ Not Met"
        ]
    }
    
    assessment_df = pd.DataFrame(assessment_data)
    st.dataframe(assessment_df, use_container_width=True)
    
    # Calculate how many criteria are met
    criteria_met = sum(1 for status in assessment_data["Status"] if "✅" in status)
    total_criteria = len(assessment_data["Status"])
    
    st.metric("Criteria Met", f"{criteria_met}/{total_criteria}")
    
    # Binary Classification Model for Loan Approval
    st.header("Loan Approval Prediction Model")
    st.markdown("This model uses machine learning to predict loan approval based on borrower characteristics and lender criteria.")
    
    # Function to create a simple binary classification model
    def create_loan_approval_model():
        # This is a placeholder for a real model that would be trained on historical data
        # In a real implementation, this model would be trained offline and loaded here
        
        # Create a simple random forest classifier
        model = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
        
        return model
    
    # Function to generate synthetic training data
    def generate_synthetic_data(n_samples=1000):
        np.random.seed(42)
        
        # Generate features
        credit_scores = np.random.randint(500, 850, n_samples)
        dti_ratios = np.random.uniform(20, 60, n_samples)
        ltv_ratios = np.random.uniform(50, 110, n_samples)
        incomes = np.random.uniform(30000, 200000, n_samples)
        employment_years = np.random.uniform(0, 20, n_samples)
        loan_amounts = np.random.uniform(50000, 1500000, n_samples)
        
        # Create feature matrix
        X = np.column_stack([credit_scores, dti_ratios, ltv_ratios, incomes, employment_years, loan_amounts])
        
        # Generate target based on typical approval criteria
        y = np.zeros(n_samples)
        
        for i in range(n_samples):
            score = 0
            # Credit score factor
            if credit_scores[i] >= 720:
                score += 3
            elif credit_scores[i] >= 680:
                score += 2
            elif credit_scores[i] >= 620:
                score += 1
            
            # DTI factor
            if dti_ratios[i] <= 36:
                score += 3
            elif dti_ratios[i] <= 43:
                score += 2
            elif dti_ratios[i] <= 50:
                score += 1
            
            # LTV factor
            if ltv_ratios[i] <= 80:
                score += 3
            elif ltv_ratios[i] <= 90:
                score += 2
            elif ltv_ratios[i] <= 95:
                score += 1
            
            # Income factor
            if incomes[i] >= 75000:
                score += 2
            elif incomes[i] >= 50000:
                score += 1
            
            # Employment factor
            if employment_years[i] >= 2:
                score += 2
            elif employment_years[i] >= 1:
                score += 1
            
            # Loan amount factor (lower is better)
            if loan_amounts[i] <= 500000:
                score += 2
            elif loan_amounts[i] <= 1000000:
                score += 1
            
            # Approval threshold
            y[i] = 1 if score >= 8 else 0
        
        return X, y
    
    # Create and train the model
    model_path = "data/loan_approval_model.joblib"
    
    # Check if model exists, otherwise create and train it
    if not os.path.exists(model_path):
        os.makedirs("data", exist_ok=True)
        
        # Generate synthetic data
        X_train, y_train = generate_synthetic_data()
        
        # Create and train model
        model = create_loan_approval_model()
        model.fit(X_train, y_train)
        
        # Save the model
        joblib.dump(model, model_path)
    else:
        # Load existing model
        model = joblib.load(model_path)
    
    # Prepare borrower data for prediction
    borrower_features = np.array([
        credit_score,
        dti_ratio,
        ltv_ratio,
        annual_income,
        employment_years if employment_years else 0,
        loan_amount
    ]).reshape(1, -1)
    
    # Make prediction
    approval_probability = model.predict_proba(borrower_features)[0, 1]
    approval_prediction = model.predict(borrower_features)[0]
    
    # Display prediction
    st.subheader("Loan Approval Prediction")
    
    prediction_col1, prediction_col2 = st.columns(2)
    
    with prediction_col1:
        # Create a gauge chart for approval probability using Plotly
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=approval_probability * 100,  # Convert to percentage
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': prediction_text, 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue", 'suffix': '%'},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 40], 'color': 'red'},
                    {'range': [40, 70], 'color': 'orange'},
                    {'range': [70, 100], 'color': 'green'}
                ],
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with prediction_col2:
        st.subheader("Key Factors Influencing Decision")
        
        # Feature importance (this would be more accurate with a real trained model)
        feature_importance = {
            "Credit Score": 0.30,
            "DTI Ratio": 0.25,
            "LTV Ratio": 0.20,
            "Annual Income": 0.10,
            "Employment History": 0.10,
            "Loan Amount": 0.05
        }
        
        # Create a bar chart of feature importance
        importance_df = pd.DataFrame({
            'Feature': list(feature_importance.keys()),
            'Importance': list(feature_importance.values())
        })
        
        fig = px.bar(
            importance_df, 
            x='Importance', 
            y='Feature',
            orientation='h',
            title='Feature Importance in Loan Decision',
            labels={'Importance': 'Relative Importance', 'Feature': ''},
            color='Importance',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Overall Assessment
    st.header("Overall Assessment")
    
    # Determine overall assessment based on criteria met and model prediction
    if criteria_met == total_criteria and approval_probability >= 0.7:
        overall_status = "Approved"
        overall_color = "green"
        recommendation = "Proceed to Loan Structuring"
    elif criteria_met >= total_criteria - 1 and approval_probability >= 0.5:
        overall_status = "Conditionally Approved"
        overall_color = "orange"
        recommendation = "Proceed with conditions"
    else:
        overall_status = "Declined"
        overall_color = "red"
        recommendation = "Consider alternative lenders or loan products"
    
    st.markdown(f"<h2 style='text-align: center; color: {overall_color};'>{overall_status}</h2>", unsafe_allow_html=True)
    
    st.subheader("Recommendation")
    st.info(recommendation)
    
    if overall_status == "Conditionally Approved":
        st.subheader("Conditions")
        conditions = []
        
        if "❌" in assessment_data["Status"][0]:  # Credit Score
            conditions.append("Improve credit score or provide explanation for recent credit issues")
        if "❌" in assessment_data["Status"][1]:  # DTI
            conditions.append("Reduce existing debt or increase income to improve DTI ratio")
        if "❌" in assessment_data["Status"][2]:  # LTV
            conditions.append("Increase down payment to reduce LTV ratio")
        if "❌" in assessment_data["Status"][3]:  # Income
            conditions.append("Provide additional income documentation or add co-borrower")
        if "❌" in assessment_data["Status"][4]:  # Employment
            conditions.append("Provide additional employment history or stability documentation")
        if "❌" in assessment_data["Status"][5]:  # Loan Amount
            conditions.append("Reduce requested loan amount")
        
        for condition in conditions:
            st.warning(f"⚠️ {condition}")
    
    # Alternative Lender Recommendations
    if overall_status == "Declined" or overall_status == "Conditionally Approved":
        st.subheader("Alternative Lender Recommendations")
        
        # Find lenders that might approve the loan
        alternative_lenders = []
        
        for lender, criteria in lender_criteria.items():
            if (credit_score >= criteria["min_credit_score"] and
                dti_ratio <= criteria["max_dti"] and
                ltv_ratio <= criteria["max_ltv"] and
                annual_income >= criteria["min_income"] and
                (employment_years is None or employment_years >= criteria["min_employment_years"]) and
                loan_amount <= criteria["max_loan_amount"]):
                
                if lender != selected_lender:
                    alternative_lenders.append(lender)
        
        if alternative_lenders:
            st.success("The following lenders may be a better fit for this application:")
            for lender in alternative_lenders:
                st.write(f"- {lender}: {lender_criteria[lender]['description']}")
        else:
            st.warning("No alternative lenders found that match the current application criteria.")
            st.write("Consider adjusting the loan amount, increasing the down payment, or improving credit factors before reapplying.")
    
    # Save lender criteria assessment
    if st.button("Save and Continue to Loan Structuring"):
        # Update session state with lender criteria data
        st.session_state.lender_criteria = {
            'lender_selection': selected_lender,
            'criteria_met': {
                'credit_score': credit_score >= lender_criteria[selected_lender]['min_credit_score'],
                'dti_ratio': dti_ratio <= lender_criteria[selected_lender]['max_dti'],
                'ltv_ratio': ltv_ratio <= lender_criteria[selected_lender]['max_ltv'],
                'annual_income': annual_income >= lender_criteria[selected_lender]['min_income'],
                'employment_years': employment_years and employment_years >= lender_criteria[selected_lender]['min_employment_years'],
                'loan_amount': loan_amount <= lender_criteria[selected_lender]['max_loan_amount']
            },
            'overall_assessment': overall_status,
            'recommendation': recommendation,
            'model_confidence': approval_probability
        }
        
        st.session_state.lender_criteria_complete = True
        st.success("Lender criteria assessment saved successfully! Please proceed to the Loan Structuring step.")
        st.balloons() 
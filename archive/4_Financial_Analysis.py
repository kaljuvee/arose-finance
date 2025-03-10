import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Financial Analysis",
    page_icon="💵",
    layout="wide"
)

st.title("Step 4: Financial Analysis")
st.markdown("Evaluate borrower's financial health and loan affordability")

# Initialize session state for financial analysis
if 'financial_analysis' not in st.session_state:
    st.session_state.financial_analysis = {
        'income_analysis': {},
        'expense_analysis': {},
        'debt_analysis': {},
        'ratios': {},
        'cash_flow': {},
        'risk_assessment': {}
    }

# Check if we have application data
has_application_data = 'application_data' in st.session_state and st.session_state.application_data.get('financial_info') and st.session_state.application_data.get('employment_info')

# Check if we have credit data
has_credit_data = 'credit_data' in st.session_state and st.session_state.credit_data.get('accounts') is not None

if not has_application_data or not has_credit_data:
    st.warning("Complete application intake and credit bureau steps before proceeding with financial analysis.")
    if not has_application_data:
        st.error("Missing application data. Please complete the Application Intake step.")
    if not has_credit_data:
        st.error("Missing credit data. Please complete the Credit Bureau Integration step.")
else:
    # Get data from session state
    application_data = st.session_state.application_data
    credit_data = st.session_state.credit_data
    
    # Income Analysis
    st.header("Income Analysis")
    
    income_col1, income_col2 = st.columns(2)
    
    with income_col1:
        # Get income from application data or use placeholder
        monthly_income = application_data['employment_info'].get('monthly_income', 0)
        if monthly_income == 0 or monthly_income is None:
            monthly_income = st.number_input("Monthly Income ($)", min_value=0, step=100, value=5000)
        else:
            monthly_income = st.number_input("Monthly Income ($)", min_value=0, step=100, value=int(monthly_income))
        
        annual_income = monthly_income * 12
        st.metric("Annual Income", f"${annual_income:,.2f}")
        
        # Additional income sources
        st.subheader("Additional Income Sources (Optional)")
        rental_income = st.number_input("Monthly Rental Income ($)", min_value=0, step=100)
        investment_income = st.number_input("Monthly Investment Income ($)", min_value=0, step=100)
        other_income = st.number_input("Other Monthly Income ($)", min_value=0, step=100)
        
        total_monthly_income = monthly_income + rental_income + investment_income + other_income
        st.metric("Total Monthly Income", f"${total_monthly_income:,.2f}")
    
    with income_col2:
        # Income stability assessment
        st.subheader("Income Stability Assessment")
        
        employment_status = application_data['employment_info'].get('employment_status', 'Unknown')
        years_employed = application_data['employment_info'].get('years_employed', 0)
        
        st.write(f"Employment Status: {employment_status}")
        st.write(f"Years at Current Employer: {years_employed}")
        
        # Income stability score (placeholder)
        stability_score = 0
        
        if employment_status == "Employed Full-Time":
            stability_score += 3
        elif employment_status == "Employed Part-Time":
            stability_score += 2
        elif employment_status == "Self-Employed":
            stability_score += 1
        
        if years_employed and years_employed > 5:
            stability_score += 3
        elif years_employed and years_employed > 2:
            stability_score += 2
        elif years_employed and years_employed > 1:
            stability_score += 1
        
        # Display stability score
        st.metric("Income Stability Score", f"{stability_score}/6")
        
        # Income verification status
        income_verified = 'documents' in st.session_state and st.session_state.documents.get('income_proof') is not None
        
        if income_verified:
            st.success("✅ Income verification documents received")
        else:
            st.warning("⚠️ Income verification pending")
    
    # Expense Analysis
    st.header("Expense Analysis")
    
    expense_col1, expense_col2 = st.columns(2)
    
    with expense_col1:
        # Get expenses from application data or use placeholder
        monthly_expenses = application_data['financial_info'].get('monthly_expenses', 0)
        if monthly_expenses == 0 or monthly_expenses is None:
            monthly_expenses = st.number_input("Total Monthly Expenses ($)", min_value=0, step=100, value=3000)
        else:
            monthly_expenses = st.number_input("Total Monthly Expenses ($)", min_value=0, step=100, value=int(monthly_expenses))
        
        # Expense breakdown
        st.subheader("Expense Breakdown")
        housing = st.number_input("Housing (Rent/Mortgage) ($)", min_value=0, step=100, value=int(monthly_expenses * 0.4))
        utilities = st.number_input("Utilities ($)", min_value=0, step=50, value=int(monthly_expenses * 0.1))
        transportation = st.number_input("Transportation ($)", min_value=0, step=50, value=int(monthly_expenses * 0.15))
        food = st.number_input("Food ($)", min_value=0, step=50, value=int(monthly_expenses * 0.15))
        insurance = st.number_input("Insurance ($)", min_value=0, step=50, value=int(monthly_expenses * 0.1))
        other_expenses = st.number_input("Other Expenses ($)", min_value=0, step=50, value=int(monthly_expenses * 0.1))
        
        # Calculate total from breakdown
        total_expenses_breakdown = housing + utilities + transportation + food + insurance + other_expenses
        
        # Update total expenses if breakdown doesn't match
        if total_expenses_breakdown != monthly_expenses:
            monthly_expenses = total_expenses_breakdown
            st.info(f"Total monthly expenses updated to ${monthly_expenses:,.2f} based on breakdown.")
    
    with expense_col2:
        # Expense visualization
        expense_data = {
            'Category': ['Housing', 'Utilities', 'Transportation', 'Food', 'Insurance', 'Other'],
            'Amount': [housing, utilities, transportation, food, insurance, other_expenses]
        }
        
        expense_df = pd.DataFrame(expense_data)
        
        fig = px.pie(expense_df, values='Amount', names='Category', title='Monthly Expense Breakdown')
        st.plotly_chart(fig, use_container_width=True)
    
    # Debt Analysis
    st.header("Debt Analysis")
    
    # Extract debt information from credit report
    if credit_data['accounts']:
        accounts = credit_data['accounts']
        total_debt = sum(account['balance'] for account in accounts)
        
        # Group debts by type
        debt_types = {}
        for account in accounts:
            account_type = account['account_type']
            if account_type in debt_types:
                debt_types[account_type] += account['balance']
            else:
                debt_types[account_type] = account['balance']
        
        debt_col1, debt_col2 = st.columns(2)
        
        with debt_col1:
            st.metric("Total Debt", f"${total_debt:,.2f}")
            
            # Display debt breakdown
            st.subheader("Debt Breakdown")
            debt_breakdown = pd.DataFrame({
                'Debt Type': list(debt_types.keys()),
                'Balance': list(debt_types.values())
            })
            st.dataframe(debt_breakdown, use_container_width=True)
        
        with debt_col2:
            # Debt visualization
            fig = px.bar(
                debt_breakdown, 
                x='Debt Type', 
                y='Balance',
                title='Debt by Type',
                labels={'Balance': 'Balance ($)', 'Debt Type': 'Type of Debt'}
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No debt information available from credit report.")
        total_debt = application_data['financial_info'].get('existing_debts', 0)
        st.metric("Total Reported Debt", f"${total_debt:,.2f}")
    
    # Financial Ratios
    st.header("Financial Ratios")
    
    # Calculate DTI (Debt-to-Income Ratio)
    monthly_debt_payments = total_debt * 0.03  # Simplified assumption for monthly payments
    dti_ratio = (monthly_debt_payments / total_monthly_income) * 100 if total_monthly_income > 0 else 0
    
    # Calculate PTI (Payment-to-Income Ratio) for the requested loan
    loan_amount = application_data['loan_info'].get('loan_amount', 0)
    loan_term = application_data['loan_info'].get('loan_term', 30)
    
    # Simple interest calculation (this would be more complex in reality)
    interest_rate = 0.05  # 5% interest rate assumption
    monthly_payment = (loan_amount * (interest_rate / 12) * (1 + interest_rate / 12) ** (loan_term * 12)) / ((1 + interest_rate / 12) ** (loan_term * 12) - 1) if loan_amount > 0 else 0
    
    pti_ratio = (monthly_payment / total_monthly_income) * 100 if total_monthly_income > 0 else 0
    
    # Calculate LTV (Loan-to-Value Ratio) - placeholder since we don't have property value
    property_value = loan_amount * 1.25  # Assumption for demonstration
    ltv_ratio = (loan_amount / property_value) * 100 if property_value > 0 else 0
    
    ratio_col1, ratio_col2, ratio_col3 = st.columns(3)
    
    with ratio_col1:
        st.metric("Debt-to-Income (DTI) Ratio", f"{dti_ratio:.2f}%")
        if dti_ratio <= 36:
            st.success("✅ DTI ratio is within acceptable range (≤36%)")
        elif dti_ratio <= 43:
            st.warning("⚠️ DTI ratio is elevated (36-43%)")
        else:
            st.error("❌ DTI ratio is high (>43%)")
    
    with ratio_col2:
        st.metric("Payment-to-Income (PTI) Ratio", f"{pti_ratio:.2f}%")
        if pti_ratio <= 28:
            st.success("✅ PTI ratio is within acceptable range (≤28%)")
        elif pti_ratio <= 33:
            st.warning("⚠️ PTI ratio is elevated (28-33%)")
        else:
            st.error("❌ PTI ratio is high (>33%)")
    
    with ratio_col3:
        st.metric("Loan-to-Value (LTV) Ratio", f"{ltv_ratio:.2f}%")
        if ltv_ratio <= 80:
            st.success("✅ LTV ratio is within acceptable range (≤80%)")
        elif ltv_ratio <= 95:
            st.warning("⚠️ LTV ratio is elevated (80-95%)")
        else:
            st.error("❌ LTV ratio is high (>95%)")
    
    # Cash Flow Analysis
    st.header("Cash Flow Analysis")
    
    # Calculate monthly cash flow
    monthly_cash_flow = total_monthly_income - monthly_expenses - monthly_debt_payments
    
    # Calculate cash flow after proposed loan payment
    cash_flow_after_loan = monthly_cash_flow - monthly_payment
    
    cash_col1, cash_col2 = st.columns(2)
    
    with cash_col1:
        st.metric("Current Monthly Cash Flow", f"${monthly_cash_flow:,.2f}")
        st.metric("Cash Flow After Loan Payment", f"${cash_flow_after_loan:,.2f}")
        
        # Cash flow assessment
        if cash_flow_after_loan > 0:
            cash_flow_status = "Positive"
            cash_flow_color = "green"
        else:
            cash_flow_status = "Negative"
            cash_flow_color = "red"
        
        st.markdown(f"Cash Flow Status: <span style='color:{cash_flow_color};font-weight:bold'>{cash_flow_status}</span>", unsafe_allow_html=True)
    
    with cash_col2:
        # Cash flow visualization
        cash_flow_data = {
            'Category': ['Income', 'Expenses', 'Debt Payments', 'Loan Payment', 'Remaining'],
            'Amount': [total_monthly_income, -monthly_expenses, -monthly_debt_payments, -monthly_payment, cash_flow_after_loan]
        }
        
        # Create a waterfall chart
        fig = go.Figure(go.Waterfall(
            name="Cash Flow",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "total"],
            x=cash_flow_data['Category'],
            y=cash_flow_data['Amount'],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "green"}},
            decreasing={"marker": {"color": "red"}},
            text=[f"${abs(val):,.2f}" for val in cash_flow_data['Amount']],
            textposition="outside"
        ))
        
        fig.update_layout(
            title="Monthly Cash Flow Analysis",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk Assessment
    st.header("Risk Assessment")
    
    # Calculate risk score based on various factors
    risk_score = 0
    max_risk_score = 10
    
    # Credit score factor (0-3 points)
    credit_score = credit_data['credit_score']
    if credit_score >= 750:
        risk_score += 3
    elif credit_score >= 700:
        risk_score += 2
    elif credit_score >= 650:
        risk_score += 1
    
    # DTI factor (0-2 points)
    if dti_ratio <= 28:
        risk_score += 2
    elif dti_ratio <= 36:
        risk_score += 1
    
    # Cash flow factor (0-2 points)
    if cash_flow_after_loan > 500:
        risk_score += 2
    elif cash_flow_after_loan > 0:
        risk_score += 1
    
    # Employment stability factor (0-2 points)
    if stability_score >= 5:
        risk_score += 2
    elif stability_score >= 3:
        risk_score += 1
    
    # LTV factor (0-1 point)
    if ltv_ratio <= 80:
        risk_score += 1
    
    # Determine risk level
    if risk_score >= 8:
        risk_level = "Low Risk"
        risk_color = "green"
    elif risk_score >= 5:
        risk_level = "Moderate Risk"
        risk_color = "orange"
    else:
        risk_level = "High Risk"
        risk_color = "red"
    
    risk_col1, risk_col2 = st.columns(2)
    
    with risk_col1:
        st.metric("Risk Score", f"{risk_score}/{max_risk_score}")
        st.markdown(f"Risk Assessment: <span style='color:{risk_color};font-weight:bold'>{risk_level}</span>", unsafe_allow_html=True)
        
        # Risk factors
        st.subheader("Risk Factors")
        risk_factors = []
        
        if credit_score < 650:
            risk_factors.append("Low credit score")
        if dti_ratio > 43:
            risk_factors.append("High debt-to-income ratio")
        if cash_flow_after_loan < 0:
            risk_factors.append("Negative cash flow")
        if stability_score < 3:
            risk_factors.append("Limited employment stability")
        if ltv_ratio > 95:
            risk_factors.append("High loan-to-value ratio")
        
        if risk_factors:
            for factor in risk_factors:
                st.warning(f"⚠️ {factor}")
        else:
            st.success("✅ No significant risk factors identified")
    
    with risk_col2:
        # Risk score visualization using Plotly
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Risk Score: {risk_level}", 'font': {'size': 24}},
            gauge={
                'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': risk_color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 5], 'color': 'red'},
                    {'range': [5, 8], 'color': 'orange'},
                    {'range': [8, 10], 'color': 'green'}
                ],
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Save financial analysis data
    if st.button("Save and Continue to Lender Criteria Assessment"):
        # Update session state with financial analysis data
        st.session_state.financial_analysis = {
            'income_analysis': {
                'monthly_income': monthly_income,
                'additional_income': rental_income + investment_income + other_income,
                'total_monthly_income': total_monthly_income,
                'stability_score': stability_score
            },
            'expense_analysis': {
                'monthly_expenses': monthly_expenses,
                'expense_breakdown': {
                    'housing': housing,
                    'utilities': utilities,
                    'transportation': transportation,
                    'food': food,
                    'insurance': insurance,
                    'other': other_expenses
                }
            },
            'debt_analysis': {
                'total_debt': total_debt,
                'monthly_debt_payments': monthly_debt_payments
            },
            'ratios': {
                'dti_ratio': dti_ratio,
                'pti_ratio': pti_ratio,
                'ltv_ratio': ltv_ratio
            },
            'cash_flow': {
                'monthly_cash_flow': monthly_cash_flow,
                'cash_flow_after_loan': cash_flow_after_loan
            },
            'risk_assessment': {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_factors': risk_factors if 'risk_factors' in locals() else []
            }
        }
        
        st.session_state.financial_analysis_complete = True
        st.success("Financial analysis data saved successfully! Please proceed to the Lender Criteria Assessment step.")
        st.balloons() 
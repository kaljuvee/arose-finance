import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Loan Structuring",
    page_icon="💲",
    layout="wide"
)

st.title("Step 6: Loan Structuring")
st.markdown("Configure loan terms based on risk assessment")

# Initialize session state for loan structuring
if 'loan_structure' not in st.session_state:
    st.session_state.loan_structure = {
        'loan_type': None,
        'interest_rate': None,
        'loan_term': None,
        'payment_schedule': None,
        'fees': {},
        'total_cost': None
    }

# Check if we have lender criteria assessment
has_lender_assessment = 'lender_criteria' in st.session_state and st.session_state.lender_criteria.get('overall_assessment')

# Check if we have application data
has_application_data = 'application_data' in st.session_state and st.session_state.application_data.get('loan_info')

if not has_lender_assessment or not has_application_data:
    st.warning("Complete previous steps before proceeding with loan structuring.")
    if not has_lender_assessment:
        st.error("Missing lender criteria assessment. Please complete the Lender Criteria Assessment step.")
    if not has_application_data:
        st.error("Missing application data. Please complete the Application Intake step.")
else:
    # Get data from session state
    lender_criteria = st.session_state.lender_criteria
    application_data = st.session_state.application_data
    financial_analysis = st.session_state.financial_analysis if 'financial_analysis' in st.session_state else None
    credit_data = st.session_state.credit_data if 'credit_data' in st.session_state else None
    
    # Display approval status
    approval_status = lender_criteria.get('overall_assessment', 'Unknown')
    
    if approval_status == "Approved":
        st.success("✅ Application Approved - Proceed with Loan Structuring")
    elif approval_status == "Conditionally Approved":
        st.warning("⚠️ Application Conditionally Approved - Proceed with Caution")
    else:
        st.error("❌ Application Declined - Loan Structuring Not Available")
        st.info("Please return to the Lender Criteria Assessment step to explore alternative options.")
        st.stop()
    
    # Loan Type Selection
    st.header("Loan Type Selection")
    
    # Get loan purpose from application
    loan_purpose = application_data['loan_info'].get('loan_purpose', 'Unknown')
    
    # Define available loan types based on purpose
    loan_types = {
        "Home Purchase": ["30-Year Fixed", "15-Year Fixed", "5/1 ARM", "7/1 ARM"],
        "Refinance": ["30-Year Fixed", "15-Year Fixed", "5/1 ARM", "7/1 ARM", "Cash-Out Refinance"],
        "Home Improvement": ["Home Equity Loan", "HELOC", "Personal Loan", "FHA 203(k)"],
        "Debt Consolidation": ["Personal Loan", "Home Equity Loan", "HELOC", "Cash-Out Refinance"],
        "Other": ["Personal Loan", "30-Year Fixed", "15-Year Fixed", "HELOC"]
    }
    
    # Default to "Other" if purpose not found
    available_loan_types = loan_types.get(loan_purpose, loan_types["Other"])
    
    loan_type_col1, loan_type_col2 = st.columns(2)
    
    with loan_type_col1:
        st.write(f"**Loan Purpose:** {loan_purpose}")
        
        selected_loan_type = st.selectbox(
            "Select Loan Type",
            available_loan_types,
            index=0,
            key="selected_loan_type"
        )
    
    with loan_type_col2:
        # Display loan type description
        loan_type_descriptions = {
            "30-Year Fixed": "A fixed-rate mortgage with a 30-year term. Offers lower monthly payments but higher total interest over the life of the loan.",
            "15-Year Fixed": "A fixed-rate mortgage with a 15-year term. Higher monthly payments but lower total interest and faster equity building.",
            "5/1 ARM": "An adjustable-rate mortgage with a fixed rate for the first 5 years, then adjusts annually. Often offers lower initial rates.",
            "7/1 ARM": "An adjustable-rate mortgage with a fixed rate for the first 7 years, then adjusts annually. Balance of stability and lower rates.",
            "Cash-Out Refinance": "Refinance your existing mortgage for more than you owe and take the difference in cash.",
            "Home Equity Loan": "A second mortgage that allows you to borrow against the equity in your home with a fixed rate and term.",
            "HELOC": "A home equity line of credit that works like a credit card, allowing you to borrow as needed up to a certain limit.",
            "Personal Loan": "An unsecured loan not tied to your home, typically with higher interest rates but faster approval.",
            "FHA 203(k)": "A government-backed loan that combines home purchase and renovation costs into a single mortgage."
        }
        
        st.info(loan_type_descriptions.get(selected_loan_type, "No description available."))
    
    # Interest Rate Determination
    st.header("Interest Rate Determination")
    
    # Get credit score and risk assessment
    credit_score = credit_data['credit_score'] if credit_data else 700  # Default if not available
    risk_level = financial_analysis['risk_assessment']['risk_level'] if financial_analysis and 'risk_assessment' in financial_analysis else "Moderate Risk"
    
    # Base interest rates by loan type (these would typically come from current market rates)
    base_rates = {
        "30-Year Fixed": 5.25,
        "15-Year Fixed": 4.50,
        "5/1 ARM": 4.75,
        "7/1 ARM": 4.85,
        "Cash-Out Refinance": 5.50,
        "Home Equity Loan": 6.25,
        "HELOC": 6.50,
        "Personal Loan": 8.75,
        "FHA 203(k)": 5.75
    }
    
    # Adjust rate based on credit score
    credit_adjustment = 0
    if credit_score >= 760:
        credit_adjustment = -0.5
    elif credit_score >= 720:
        credit_adjustment = -0.25
    elif credit_score >= 680:
        credit_adjustment = 0
    elif credit_score >= 640:
        credit_adjustment = 0.25
    elif credit_score >= 600:
        credit_adjustment = 0.75
    else:
        credit_adjustment = 1.5
    
    # Adjust rate based on risk level
    risk_adjustment = 0
    if risk_level == "Low Risk":
        risk_adjustment = -0.125
    elif risk_level == "Moderate Risk":
        risk_adjustment = 0.125
    else:  # High Risk
        risk_adjustment = 0.375
    
    # Calculate adjusted interest rate
    base_rate = base_rates.get(selected_loan_type, 5.0)
    adjusted_rate = base_rate + credit_adjustment + risk_adjustment
    
    # Allow manual adjustment within a reasonable range
    rate_col1, rate_col2 = st.columns(2)
    
    with rate_col1:
        st.write("**Interest Rate Factors:**")
        st.write(f"- Base Rate for {selected_loan_type}: {base_rate:.2f}%")
        st.write(f"- Credit Score Adjustment: {credit_adjustment:+.2f}%")
        st.write(f"- Risk Assessment Adjustment: {risk_adjustment:+.2f}%")
        st.write(f"- Calculated Rate: {adjusted_rate:.2f}%")
    
    with rate_col2:
        # Allow manual adjustment within a reasonable range
        min_rate = max(adjusted_rate - 0.5, base_rate - 1.0)
        max_rate = min(adjusted_rate + 1.0, base_rate + 3.0)
        
        final_rate = st.slider(
            "Final Interest Rate (%)",
            min_value=float(f"{min_rate:.2f}"),
            max_value=float(f"{max_rate:.2f}"),
            value=float(f"{adjusted_rate:.2f}"),
            step=0.125,
            key="final_interest_rate"
        )
        
        if final_rate != adjusted_rate:
            st.info(f"Rate manually adjusted from {adjusted_rate:.2f}% to {final_rate:.2f}%")
    
    # Loan Term Selection
    st.header("Loan Term Selection")
    
    # Available terms based on loan type
    term_options = {
        "30-Year Fixed": [30],
        "15-Year Fixed": [15],
        "5/1 ARM": [30],
        "7/1 ARM": [30],
        "Cash-Out Refinance": [15, 20, 30],
        "Home Equity Loan": [5, 10, 15, 20],
        "HELOC": [10, 15, 20, 30],
        "Personal Loan": [3, 5, 7, 10],
        "FHA 203(k)": [15, 30]
    }
    
    available_terms = term_options.get(selected_loan_type, [30, 15])
    
    # Get loan amount from application
    loan_amount = application_data['loan_info'].get('loan_amount', 100000)
    
    term_col1, term_col2 = st.columns(2)
    
    with term_col1:
        selected_term = st.selectbox(
            "Select Loan Term (Years)",
            available_terms,
            index=0,
            key="selected_term"
        )
        
        # Calculate monthly payment
        monthly_payment = calculate_monthly_payment(loan_amount, final_rate, selected_term)
        
        st.metric("Estimated Monthly Payment", f"${monthly_payment:,.2f}")
    
    with term_col2:
        # Show total interest paid
        total_interest = (monthly_payment * 12 * selected_term) - loan_amount
        total_cost = loan_amount + total_interest
        
        st.metric("Total Interest Paid", f"${total_interest:,.2f}")
        st.metric("Total Cost of Loan", f"${total_cost:,.2f}")
    
    # Payment Schedule
    st.header("Payment Schedule")
    
    # Generate amortization schedule
    schedule = generate_amortization_schedule(loan_amount, final_rate, selected_term)
    
    # Display interactive chart
    fig = px.line(
        schedule, 
        x='Payment Number', 
        y=['Principal Balance', 'Cumulative Principal', 'Cumulative Interest'],
        title='Loan Amortization Schedule',
        labels={'value': 'Amount ($)', 'Payment Number': 'Payment Number', 'variable': 'Category'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display amortization table (first 12 months and summary)
    st.subheader("Amortization Table")
    
    # First year payments
    st.write("**First Year Payments:**")
    first_year = schedule.head(12).copy()
    first_year['Date'] = [datetime.now() + timedelta(days=30*i) for i in range(1, 13)]
    first_year['Date'] = first_year['Date'].dt.strftime('%b %Y')
    st.dataframe(first_year[['Payment Number', 'Date', 'Payment', 'Principal', 'Interest', 'Principal Balance']], use_container_width=True)
    
    # Summary by year
    st.write("**Annual Summary:**")
    annual_summary = schedule.groupby(schedule['Payment Number'].apply(lambda x: (x-1)//12 + 1)).agg({
        'Payment': 'sum',
        'Principal': 'sum',
        'Interest': 'sum',
        'Principal Balance': 'last'
    }).reset_index()
    annual_summary.rename(columns={'Payment Number': 'Year'}, inplace=True)
    
    # Only show first 5 years and last year
    if len(annual_summary) > 6:
        annual_summary = pd.concat([annual_summary.head(5), annual_summary.tail(1)])
    
    st.dataframe(annual_summary, use_container_width=True)
    
    # Loan Fees and Closing Costs
    st.header("Loan Fees and Closing Costs")
    
    # Define standard fees
    standard_fees = {
        "Origination Fee": loan_amount * 0.01,
        "Application Fee": 500,
        "Credit Report Fee": 50,
        "Appraisal Fee": 500,
        "Title Search and Insurance": loan_amount * 0.005,
        "Recording Fee": 125,
        "Underwriting Fee": 750
    }
    
    fee_col1, fee_col2 = st.columns(2)
    
    with fee_col1:
        st.subheader("Standard Fees")
        
        # Allow adjustment of standard fees
        adjusted_fees = {}
        for fee_name, fee_amount in standard_fees.items():
            adjusted_amount = st.number_input(
                f"{fee_name} ($)",
                min_value=0.0,
                max_value=fee_amount * 2,
                value=fee_amount,
                step=25.0,
                key=f"fee_{fee_name.replace(' ', '_').lower()}"
            )
            adjusted_fees[fee_name] = adjusted_amount
    
    with fee_col2:
        st.subheader("Additional Fees (Optional)")
        
        # Allow adding custom fees
        custom_fee_name = st.text_input("Fee Name", key="custom_fee_name")
        custom_fee_amount = st.number_input("Fee Amount ($)", min_value=0.0, step=25.0, key="custom_fee_amount")
        
        if st.button("Add Fee"):
            if custom_fee_name and custom_fee_amount > 0:
                adjusted_fees[custom_fee_name] = custom_fee_amount
                st.success(f"Added {custom_fee_name}: ${custom_fee_amount:.2f}")
        
        # Calculate total fees
        total_fees = sum(adjusted_fees.values())
        st.metric("Total Fees and Closing Costs", f"${total_fees:,.2f}")
        
        # Calculate cash needed to close
        down_payment = loan_amount * 0.20  # Assuming 20% down payment
        cash_to_close = down_payment + total_fees
        
        st.metric("Estimated Cash to Close", f"${cash_to_close:,.2f}")
    
    # Loan Summary
    st.header("Loan Summary")
    
    summary_col1, summary_col2 = st.columns(2)
    
    with summary_col1:
        st.subheader("Loan Details")
        st.write(f"**Loan Type:** {selected_loan_type}")
        st.write(f"**Loan Amount:** ${loan_amount:,.2f}")
        st.write(f"**Interest Rate:** {final_rate:.3f}%")
        st.write(f"**Loan Term:** {selected_term} years")
        st.write(f"**Monthly Payment:** ${monthly_payment:,.2f}")
        st.write(f"**Total Interest:** ${total_interest:,.2f}")
        st.write(f"**Total Cost of Loan:** ${total_cost:,.2f}")
    
    with summary_col2:
        st.subheader("Closing Costs")
        
        # Display fees as a pie chart
        fee_data = pd.DataFrame({
            'Fee': list(adjusted_fees.keys()),
            'Amount': list(adjusted_fees.values())
        })
        
        fig = px.pie(
            fee_data, 
            values='Amount', 
            names='Fee', 
            title='Closing Costs Breakdown'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Save loan structure
    if st.button("Save and Continue to Approval Process"):
        # Update session state with loan structure data
        st.session_state.loan_structure = {
            'loan_type': selected_loan_type,
            'interest_rate': final_rate,
            'loan_term': selected_term,
            'monthly_payment': monthly_payment,
            'payment_schedule': schedule.to_dict(),
            'fees': adjusted_fees,
            'total_fees': total_fees,
            'total_interest': total_interest,
            'total_cost': total_cost,
            'cash_to_close': cash_to_close
        }
        
        st.session_state.loan_structure_complete = True
        st.success("Loan structure saved successfully! Please proceed to the Approval Process step.")
        st.balloons()

# Helper function to calculate monthly payment
def calculate_monthly_payment(loan_amount, annual_interest_rate, term_years):
    # Convert annual interest rate to monthly and decimal form
    monthly_interest_rate = annual_interest_rate / 100 / 12
    term_months = term_years * 12
    
    # Calculate monthly payment using the loan payment formula
    if monthly_interest_rate == 0:
        return loan_amount / term_months
    
    monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** term_months) / ((1 + monthly_interest_rate) ** term_months - 1)
    
    return monthly_payment

# Helper function to generate amortization schedule
def generate_amortization_schedule(loan_amount, annual_interest_rate, term_years):
    # Convert annual interest rate to monthly and decimal form
    monthly_interest_rate = annual_interest_rate / 100 / 12
    term_months = term_years * 12
    
    # Calculate monthly payment
    monthly_payment = calculate_monthly_payment(loan_amount, annual_interest_rate, term_years)
    
    # Initialize variables for tracking
    remaining_balance = loan_amount
    schedule_data = []
    cumulative_principal = 0
    cumulative_interest = 0
    
    # Generate amortization schedule
    for payment_num in range(1, term_months + 1):
        # Calculate interest and principal for this payment
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        
        # Update remaining balance
        remaining_balance -= principal_payment
        
        # Update cumulative totals
        cumulative_principal += principal_payment
        cumulative_interest += interest_payment
        
        # Add data to schedule
        schedule_data.append({
            'Payment Number': payment_num,
            'Payment': monthly_payment,
            'Principal': principal_payment,
            'Interest': interest_payment,
            'Principal Balance': remaining_balance,
            'Cumulative Principal': cumulative_principal,
            'Cumulative Interest': cumulative_interest
        })
    
    # Convert to DataFrame
    schedule_df = pd.DataFrame(schedule_data)
    
    return schedule_df 
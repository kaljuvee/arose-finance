import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import time
import random

st.set_page_config(
    page_title="Lender Communication",
    page_icon="📧",
    layout="wide"
)

st.title("Step 7: Lender Communication")
st.markdown("Send bespoke emails to lenders and collect their feedback")

# Check if previous steps are completed
if 'lender_matching' not in st.session_state:
    st.warning("Please complete Step 5: Lender Matching first.")
    st.stop()

# Initialize session state for lender communication
if 'lender_communication' not in st.session_state:
    st.session_state.lender_communication = {
        'emails_sent': [],
        'lender_responses': {},
        'feedback_collected': {},
        'template_updates': []
    }

# Get matched lenders from previous step
matched_lenders = st.session_state.lender_matching.get('matched_lenders', [])
if not matched_lenders:
    st.error("No matched lenders found. Please complete the Lender Matching step properly.")
    st.stop()

# Get verified client profile
verified_profile = st.session_state.verified_profile if 'verified_profile' in st.session_state else {}

# Display client profile summary
st.header("Client Profile Summary")
if verified_profile:
    client_profile = verified_profile.get('client_profile', {})
    loan_requirements = verified_profile.get('loan_requirements', {})
    property_details = verified_profile.get('property_details', {})
    financial_profile = verified_profile.get('financial_profile', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Client Information")
        st.write(f"**Name:** {client_profile.get('first_name', '')} {client_profile.get('last_name', '')}")
        st.write(f"**Email:** {client_profile.get('email', '')}")
        st.write(f"**Phone:** {client_profile.get('phone', '')}")
        
        st.subheader("Loan Requirements")
        st.write(f"**Loan Purpose:** {loan_requirements.get('loan_purpose', '')}")
        st.write(f"**Loan Amount:** ${loan_requirements.get('loan_amount', 0):,}")
        st.write(f"**Down Payment:** ${loan_requirements.get('down_payment', 0):,}")
    
    with col2:
        st.subheader("Property Details")
        st.write(f"**Property Type:** {property_details.get('property_type', '')}")
        st.write(f"**Property Value:** ${property_details.get('property_value', 0):,}")
        st.write(f"**Property Use:** {property_details.get('property_use', '')}")
        
        st.subheader("Financial Profile")
        st.write(f"**Employment:** {financial_profile.get('employment_status', '')}")
        st.write(f"**Annual Income:** ${financial_profile.get('annual_income', 0):,}")
        st.write(f"**Credit Score:** {financial_profile.get('credit_score', '')}")
else:
    st.warning("Client profile not found. Some information may be missing.")

# Display matched lenders
st.header("Matched Lenders")
st.info("These lenders were matched to the client profile in the previous step.")

# Convert matched lenders to DataFrame if it's not already
if isinstance(matched_lenders, list):
    matched_df = pd.DataFrame(matched_lenders)
else:
    matched_df = matched_lenders

# Display top matched lenders
top_lenders = matched_df.nlargest(5, "Final Score") if "Final Score" in matched_df.columns else matched_df.head(5)
st.dataframe(top_lenders, use_container_width=True)

# Email Template Generation
st.header("Email Template Generation")
st.info("Generate bespoke email templates for each lender based on their specific requirements.")

# Function to generate email templates
def generate_email_template(lender, client_profile, loan_requirements, property_details, financial_profile):
    # Get lender name
    lender_name = lender["Lender"] if isinstance(lender, dict) else lender
    
    # Generate salutation
    salutation = f"Dear {lender_name} Team,"
    
    # Generate introduction
    introduction = f"""
    I am writing to submit a loan application for my client, {client_profile.get('first_name', '')} {client_profile.get('last_name', '')}, 
    who is seeking a {loan_requirements.get('loan_purpose', '')} loan for a {property_details.get('property_type', '')} property.
    """
    
    # Generate client profile section
    client_section = f"""
    ## Client Profile
    - Name: {client_profile.get('first_name', '')} {client_profile.get('last_name', '')}
    - Credit Score: {financial_profile.get('credit_score', '')}
    - Employment: {financial_profile.get('employment_status', '')} at {financial_profile.get('employer_name', '')} for {financial_profile.get('years_employed', '')} years
    - Annual Income: ${financial_profile.get('annual_income', 0):,}
    """
    
    # Generate loan details section
    loan_section = f"""
    ## Loan Requirements
    - Loan Purpose: {loan_requirements.get('loan_purpose', '')}
    - Loan Amount: ${loan_requirements.get('loan_amount', 0):,}
    - Down Payment: ${loan_requirements.get('down_payment', 0):,}
    - Preferred Term: {loan_requirements.get('loan_term_preference', '')}
    """
    
    # Generate property details section
    property_section = f"""
    ## Property Details
    - Property Type: {property_details.get('property_type', '')}
    - Property Value: ${property_details.get('property_value', 0):,}
    - Property Use: {property_details.get('property_use', '')}
    - Property Condition: {property_details.get('property_condition', '')}
    """
    
    # Generate lender-specific section
    lender_specific = ""
    if "Prime" in lender_name:
        lender_specific = """
        Based on your premium loan program requirements, I believe this client is an excellent match due to their strong credit profile and stable employment history.
        """
    elif "Standard" in lender_name:
        lender_specific = """
        Your standard loan program appears to be a good fit for this client's needs, offering competitive rates and suitable terms.
        """
    elif "Flexible" in lender_name:
        lender_specific = """
        Your flexible loan program would be ideal for this client, providing the adaptability needed for their specific situation.
        """
    elif "Bank" in lender_name:
        lender_specific = """
        As a valued banking partner, I believe your loan products would be well-suited for this client's financial profile and property requirements.
        """
    elif "Credit Union" in lender_name:
        lender_specific = """
        Your member-focused approach and competitive rates would be beneficial for this client's loan needs.
        """
    elif "Specialist" in lender_name:
        lender_specific = """
        Given your expertise in specialized lending scenarios, I believe you could offer optimal terms for this client's unique situation.
        """
    
    # Generate closing
    closing = """
    I have attached all relevant documentation for your review. Please let me know if you require any additional information.
    
    I look forward to your response regarding this application. You can reply directly to this email with your decision or questions.
    
    Thank you for your consideration.
    
    Best regards,
    [Broker Name]
    Arose Finance
    """
    
    # Combine all sections
    full_template = f"{salutation}\n\n{introduction}\n\n{client_section}\n\n{loan_section}\n\n{property_section}\n\n{lender_specific}\n\n{closing}"
    
    return full_template

# Generate and display email templates for top lenders
st.subheader("Email Templates")

# Create tabs for each lender
lender_tabs = st.tabs([lender["Lender"] if isinstance(lender, dict) else str(lender) for lender in top_lenders.iterrows()])

# Generate templates for each lender
email_templates = {}
for i, (_, lender) in enumerate(top_lenders.iterrows()):
    with lender_tabs[i]:
        lender_name = lender["Lender"]
        
        # Generate template
        template = generate_email_template(
            lender,
            client_profile,
            loan_requirements,
            property_details,
            financial_profile
        )
        
        # Store template
        email_templates[lender_name] = template
        
        # Display template
        st.text_area(
            f"Email Template for {lender_name}",
            value=template,
            height=400,
            key=f"template_{i}"
        )
        
        # Allow customization
        st.checkbox(f"Customize template for {lender_name}", key=f"customize_{i}")
        
        if st.session_state[f"customize_{i}"]:
            custom_template = st.text_area(
                "Customized Template",
                value=template,
                height=400,
                key=f"custom_template_{i}"
            )
            email_templates[lender_name] = custom_template

# Document Selection
st.header("Document Selection")
st.info("Select which documents to include with each lender's email.")

# List available documents (from previous steps)
available_documents = [
    "ID Verification",
    "Income Proof",
    "Bank Statements",
    "Tax Returns",
    "Property Information",
    "Credit Report",
    "Application Form",
    "Fact-Find Summary"
]

# Create document selection for each lender
document_selection = {}
for i, (_, lender) in enumerate(top_lenders.iterrows()):
    lender_name = lender["Lender"]
    
    st.subheader(f"Documents for {lender_name}")
    
    # Recommend documents based on lender type
    recommended_docs = []
    if "Prime" in lender_name:
        recommended_docs = ["ID Verification", "Income Proof", "Bank Statements", "Tax Returns", "Property Information", "Credit Report"]
    elif "Standard" in lender_name:
        recommended_docs = ["ID Verification", "Income Proof", "Bank Statements", "Property Information", "Credit Report"]
    elif "Flexible" in lender_name:
        recommended_docs = ["ID Verification", "Income Proof", "Bank Statements", "Application Form"]
    elif "Bank" in lender_name:
        recommended_docs = ["ID Verification", "Income Proof", "Bank Statements", "Tax Returns", "Property Information"]
    elif "Credit Union" in lender_name:
        recommended_docs = ["ID Verification", "Income Proof", "Bank Statements", "Application Form"]
    elif "Specialist" in lender_name:
        recommended_docs = ["ID Verification", "Income Proof", "Application Form", "Fact-Find Summary"]
    
    # Allow selection with recommended docs pre-selected
    selected_docs = st.multiselect(
        f"Select documents to include for {lender_name}",
        available_documents,
        default=recommended_docs,
        key=f"docs_{i}"
    )
    
    document_selection[lender_name] = selected_docs

# Email Sending Simulation
st.header("Email Sending")
st.info("Send the emails to the selected lenders.")

# Select which lenders to email
lenders_to_email = st.multiselect(
    "Select lenders to email",
    [lender["Lender"] for _, lender in top_lenders.iterrows()],
    default=[lender["Lender"] for _, lender in top_lenders.iterrows()],
    key="lenders_to_email"
)

# Send emails button
if st.button("Send Emails to Selected Lenders"):
    with st.spinner("Sending emails..."):
        # Simulate email sending
        time.sleep(2)
        
        # Record emails sent
        emails_sent = []
        for lender_name in lenders_to_email:
            emails_sent.append({
                "lender": lender_name,
                "template": email_templates[lender_name],
                "documents": document_selection[lender_name],
                "sent_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # Store in session state
        st.session_state.lender_communication['emails_sent'] = emails_sent
        
        st.success(f"✅ Emails successfully sent to {len(emails_sent)} lenders!")

# Lender Response Simulation
if 'emails_sent' in st.session_state.lender_communication and st.session_state.lender_communication['emails_sent']:
    st.header("Lender Responses")
    st.info("This section simulates lender responses to the emails sent.")
    
    # Check if we already have responses
    if not st.session_state.lender_communication.get('lender_responses'):
        # Simulate lender responses
        if st.button("Simulate Lender Responses"):
            with st.spinner("Receiving lender responses..."):
                # Simulate response delay
                time.sleep(3)
                
                # Generate random responses
                lender_responses = {}
                for email in st.session_state.lender_communication['emails_sent']:
                    lender_name = email["lender"]
                    
                    # Determine response type based on lender match percentage
                    lender_match = next((l for _, l in top_lenders.iterrows() if l["Lender"] == lender_name), None)
                    match_score = lender_match["Final Score"] if lender_match is not None and "Final Score" in lender_match else 50
                    
                    # Higher match score = higher chance of approval
                    yes_prob = match_score / 100
                    maybe_prob = (100 - match_score) / 200
                    no_prob = 1 - yes_prob - maybe_prob
                    
                    response_type = np.random.choice(
                        ["Yes", "Maybe", "No"],
                        p=[yes_prob, maybe_prob, no_prob]
                    )
                    
                    # Generate response details
                    if response_type == "Yes":
                        details = {
                            "decision": "Yes",
                            "notes": "We are pleased to offer your client a loan based on the information provided.",
                            "dip_attached": True,
                            "further_docs_required": random.sample(["Proof of Deposit", "Property Valuation", "Insurance Details"], k=random.randint(1, 3)),
                            "response_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    elif response_type == "Maybe":
                        details = {
                            "decision": "Maybe",
                            "notes": "We need additional information before making a final decision.",
                            "questions": random.sample([
                                "Can you provide more details about the client's employment history?",
                                "We need clarification on the source of the down payment.",
                                "Please provide more information about the property condition.",
                                "What is the client's debt-to-income ratio?",
                                "Can you explain the purpose of this loan in more detail?"
                            ], k=random.randint(2, 4)),
                            "response_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    else:  # No
                        details = {
                            "decision": "No",
                            "notes": "Unfortunately, we are unable to proceed with this application at this time.",
                            "reasons": random.sample([
                                "Credit score below our minimum requirements",
                                "Loan amount exceeds our lending limits for this property type",
                                "Insufficient income for the requested loan amount",
                                "Property type not eligible for our loan programs",
                                "Debt-to-income ratio too high"
                            ], k=random.randint(1, 3)),
                            "response_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    
                    lender_responses[lender_name] = details
                
                # Store in session state
                st.session_state.lender_communication['lender_responses'] = lender_responses
                
                st.success("✅ Lender responses received!")
    
    # Display lender responses
    if st.session_state.lender_communication.get('lender_responses'):
        lender_responses = st.session_state.lender_communication['lender_responses']
        
        # Create tabs for each lender response
        response_tabs = st.tabs(list(lender_responses.keys()))
        
        for i, (lender_name, response) in enumerate(lender_responses.items()):
            with response_tabs[i]:
                # Display response based on decision
                if response["decision"] == "Yes":
                    st.success(f"✅ {lender_name} has approved the loan application!")
                    st.write(f"**Notes:** {response['notes']}")
                    
                    st.subheader("Decision in Principle")
                    if response["dip_attached"]:
                        st.info("Decision in Principle document is attached.")
                    
                    st.subheader("Further Documentation Required")
                    for doc in response["further_docs_required"]:
                        st.write(f"- {doc}")
                    
                    # Algorithm learning feedback
                    st.subheader("Algorithm Feedback")
                    st.write("✓ The matching algorithm has been reinforced by this successful match.")
                
                elif response["decision"] == "Maybe":
                    st.warning(f"⚠️ {lender_name} needs more information before making a decision.")
                    st.write(f"**Notes:** {response['notes']}")
                    
                    st.subheader("Additional Questions")
                    for question in response["questions"]:
                        st.text_input(f"Response to: {question}", key=f"q_{i}_{question}")
                    
                    if st.button(f"Send Responses to {lender_name}", key=f"send_responses_{i}"):
                        st.success("Responses sent successfully!")
                        
                        # Algorithm learning feedback
                        st.subheader("Algorithm Feedback")
                        st.write("✓ The algorithm has updated its question set to include these questions for future applications.")
                        
                        # Update template for future use
                        template_update = f"Updated email template for {lender_name} to include answers to frequently asked questions."
                        if 'template_updates' not in st.session_state.lender_communication:
                            st.session_state.lender_communication['template_updates'] = []
                        st.session_state.lender_communication['template_updates'].append(template_update)
                
                else:  # No
                    st.error(f"❌ {lender_name} has declined the loan application.")
                    st.write(f"**Notes:** {response['notes']}")
                    
                    st.subheader("Reasons for Decline")
                    for reason in response["reasons"]:
                        st.write(f"- {reason}")
                    
                    # Algorithm learning feedback
                    st.subheader("Algorithm Feedback")
                    st.write("✓ The algorithm has been updated to incorporate these decline reasons into its matching criteria.")
                    
                    # Collect feedback for algorithm improvement
                    feedback = st.text_area(f"Additional feedback for {lender_name}", key=f"feedback_{i}")
                    if st.button(f"Submit Feedback for {lender_name}", key=f"submit_feedback_{i}"):
                        if 'feedback_collected' not in st.session_state.lender_communication:
                            st.session_state.lender_communication['feedback_collected'] = {}
                        st.session_state.lender_communication['feedback_collected'][lender_name] = feedback
                        st.success("Feedback submitted successfully!")

# Feedback Collection Center
st.header("Lender Feedback Collection Center")
st.info("This centralized response center collects feedback from lenders to improve the matching algorithm.")

# Display feedback statistics
if st.session_state.lender_communication.get('lender_responses'):
    lender_responses = st.session_state.lender_communication['lender_responses']
    
    # Calculate statistics
    total_responses = len(lender_responses)
    yes_responses = sum(1 for r in lender_responses.values() if r["decision"] == "Yes")
    maybe_responses = sum(1 for r in lender_responses.values() if r["decision"] == "Maybe")
    no_responses = sum(1 for r in lender_responses.values() if r["decision"] == "No")
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Approvals", f"{yes_responses}/{total_responses}", f"{yes_responses/total_responses*100:.1f}%")
    
    with col2:
        st.metric("Requests for More Info", f"{maybe_responses}/{total_responses}", f"{maybe_responses/total_responses*100:.1f}%")
    
    with col3:
        st.metric("Declines", f"{no_responses}/{total_responses}", f"{no_responses/total_responses*100:.1f}%")
    
    # Display feedback impact
    st.subheader("Feedback Impact on Algorithm")
    
    # Display algorithm updates based on feedback
    if maybe_responses > 0:
        st.info("📝 Question sets have been updated based on lender requests for additional information.")
        
        # Show sample questions added to future question sets
        all_questions = []
        for response in lender_responses.values():
            if response["decision"] == "Maybe" and "questions" in response:
                all_questions.extend(response["questions"])
        
        if all_questions:
            st.write("**Questions added to future question sets:**")
            for question in list(set(all_questions))[:3]:  # Show up to 3 unique questions
                st.write(f"- {question}")
    
    if no_responses > 0:
        st.warning("⚠️ Matching criteria have been adjusted based on decline reasons.")
        
        # Show sample criteria adjustments
        all_reasons = []
        for response in lender_responses.values():
            if response["decision"] == "No" and "reasons" in response:
                all_reasons.extend(response["reasons"])
        
        if all_reasons:
            st.write("**Matching criteria adjustments:**")
            for reason in list(set(all_reasons))[:3]:  # Show up to 3 unique reasons
                if "credit score" in reason.lower():
                    st.write(f"- Adjusted credit score threshold for certain lenders")
                elif "income" in reason.lower():
                    st.write(f"- Updated income requirements in matching algorithm")
                elif "debt-to-income" in reason.lower() or "dti" in reason.lower():
                    st.write(f"- Refined DTI ratio limits in lender matching")
                elif "property" in reason.lower():
                    st.write(f"- Updated property type eligibility criteria")
                else:
                    st.write(f"- Added new variable to matching matrix based on: {reason}")
    
    if yes_responses > 0:
        st.success("✅ Matching algorithm has been reinforced by successful approvals.")

# Save and Continue Button
if st.button("Save and Continue to Client Communication"):
    st.success("Lender communication data saved successfully! Please proceed to the Client Communication step.")
    st.balloons() 
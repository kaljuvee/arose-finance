import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import time
import random

st.set_page_config(
    page_title="Client Communication",
    page_icon="📨",
    layout="wide"
)

st.title("Step 8: Client Communication")
st.markdown("Present lender feedback to client and send templated email")

# Check if previous steps are completed
if 'lender_communication' not in st.session_state:
    st.warning("Please complete Step 7: Lender Communication first.")
    st.stop()

# Initialize session state for client communication
if 'client_communication' not in st.session_state:
    st.session_state.client_communication = {
        'email_template': '',
        'email_sent': False,
        'email_timestamp': None,
        'selected_offers': []
    }

# Get lender responses from previous step
lender_responses = st.session_state.lender_communication.get('lender_responses', {})
if not lender_responses:
    st.error("No lender responses found. Please complete the Lender Communication step properly.")
    st.stop()

# Get client profile
verified_profile = st.session_state.verified_profile if 'verified_profile' in st.session_state else {}
if not verified_profile:
    st.warning("Client profile not found. Some information may be missing.")
    client_profile = {"first_name": "Client", "last_name": "", "email": "client@example.com"}
else:
    client_profile = verified_profile.get('client_profile', {})

# Display client information
st.header("Client Information")
col1, col2 = st.columns(2)

with col1:
    st.write(f"**Name:** {client_profile.get('first_name', '')} {client_profile.get('last_name', '')}")
    st.write(f"**Email:** {client_profile.get('email', '')}")
    st.write(f"**Phone:** {client_profile.get('phone', '')}")

with col2:
    if 'fact_find_data' in st.session_state:
        meeting_details = st.session_state.fact_find_data.get('meeting_details', {})
        st.write(f"**Initial Meeting Date:** {meeting_details.get('meeting_date', 'Not recorded')}")
        st.write(f"**Broker:** {meeting_details.get('broker_name', 'Not recorded')}")
    else:
        st.write("**Meeting Details:** Not available")

# Lender Response Summary
st.header("Lender Response Summary")
st.info("This section summarizes the responses received from lenders.")

# Calculate response statistics
total_responses = len(lender_responses)
yes_responses = sum(1 for r in lender_responses.values() if r["decision"] == "Yes")
maybe_responses = sum(1 for r in lender_responses.values() if r["decision"] == "Maybe")
no_responses = sum(1 for r in lender_responses.values() if r["decision"] == "No")

# Display statistics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Approvals", yes_responses, f"{yes_responses/total_responses*100:.1f}%" if total_responses > 0 else "0%")

with col2:
    st.metric("Requests for More Info", maybe_responses, f"{maybe_responses/total_responses*100:.1f}%" if total_responses > 0 else "0%")

with col3:
    st.metric("Declines", no_responses, f"{no_responses/total_responses*100:.1f}%" if total_responses > 0 else "0%")

# Create a visual representation of responses
response_data = pd.DataFrame({
    "Lender": list(lender_responses.keys()),
    "Decision": [r["decision"] for r in lender_responses.values()]
})

# Create a color map for decisions
color_map = {"Yes": "#28a745", "Maybe": "#ffc107", "No": "#dc3545"}

# Create a horizontal bar chart
fig = px.bar(
    response_data,
    y="Lender",
    x=[1] * len(response_data),  # All bars same length
    color="Decision",
    color_discrete_map=color_map,
    orientation='h',
    title="Lender Responses at a Glance"
)

fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    margin=dict(l=0, r=0, t=40, b=0),
    height=300,
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

# Detailed Lender Responses
st.header("Detailed Lender Responses")

# Create tabs for different response types
tab1, tab2, tab3 = st.tabs(["Approvals", "Requests for More Info", "Declines"])

with tab1:
    # Filter for approvals
    approvals = {k: v for k, v in lender_responses.items() if v["decision"] == "Yes"}
    
    if approvals:
        st.success(f"✅ {len(approvals)} lenders have approved the loan application!")
        
        # Display each approval
        for lender_name, response in approvals.items():
            st.subheader(lender_name)
            st.write(f"**Notes:** {response['notes']}")
            
            # Display DIP status
            if response.get("dip_attached", False):
                st.info("Decision in Principle document is available.")
            
            # Display further documentation required
            if "further_docs_required" in response and response["further_docs_required"]:
                st.write("**Further Documentation Required:**")
                for doc in response["further_docs_required"]:
                    st.write(f"- {doc}")
            
            # Option to select this offer
            st.checkbox(f"Include this offer in client communication", value=True, key=f"select_approval_{lender_name}")
    else:
        st.warning("No approvals received yet.")

with tab2:
    # Filter for maybes
    maybes = {k: v for k, v in lender_responses.items() if v["decision"] == "Maybe"}
    
    if maybes:
        st.warning(f"⚠️ {len(maybes)} lenders need more information before making a decision.")
        
        # Display each maybe
        for lender_name, response in maybes.items():
            st.subheader(lender_name)
            st.write(f"**Notes:** {response['notes']}")
            
            # Display questions
            if "questions" in response and response["questions"]:
                st.write("**Additional Questions:**")
                for question in response["questions"]:
                    st.write(f"- {question}")
            
            # Option to include in client communication
            st.checkbox(f"Include this response in client communication", value=True, key=f"select_maybe_{lender_name}")
    else:
        st.info("No lenders have requested additional information.")

with tab3:
    # Filter for declines
    declines = {k: v for k, v in lender_responses.items() if v["decision"] == "No"}
    
    if declines:
        st.error(f"❌ {len(declines)} lenders have declined the loan application.")
        
        # Display each decline
        for lender_name, response in declines.items():
            st.subheader(lender_name)
            st.write(f"**Notes:** {response['notes']}")
            
            # Display reasons
            if "reasons" in response and response["reasons"]:
                st.write("**Reasons for Decline:**")
                for reason in response["reasons"]:
                    st.write(f"- {reason}")
            
            # Option to include in client communication
            st.checkbox(f"Include this response in client communication", value=False, key=f"select_decline_{lender_name}")
    else:
        st.success("No lenders have declined the application.")

# Email Template Generation
st.header("Client Email Template")
st.info("Generate an email template to send to the client with the lender responses.")

# Function to generate client email template
def generate_client_email(client_name, approvals, maybes, declines, include_approvals=True, include_maybes=True, include_declines=False):
    # Generate salutation
    salutation = f"Dear {client_name},"
    
    # Generate introduction
    introduction = f"""
    Thank you for your loan application with Arose Finance. We have received responses from several lenders regarding your application, and I'm pleased to provide you with a summary of their feedback.
    """
    
    # Generate approvals section
    approvals_section = ""
    if approvals and include_approvals:
        approvals_section = """
        ## Approved Offers
        
        I'm pleased to inform you that we have received the following approvals:
        """
        
        for lender_name, response in approvals.items():
            approvals_section += f"""
            ### {lender_name}
            - {response['notes']}
            """
            
            if "further_docs_required" in response and response["further_docs_required"]:
                approvals_section += """
                - Further documentation required:
                """
                for doc in response["further_docs_required"]:
                    approvals_section += f"""
                  - {doc}
                    """
    
    # Generate maybes section
    maybes_section = ""
    if maybes and include_maybes:
        maybes_section = """
        ## Lenders Requesting Additional Information
        
        The following lenders have expressed interest but require additional information:
        """
        
        for lender_name, response in maybes.items():
            maybes_section += f"""
            ### {lender_name}
            - {response['notes']}
            """
            
            if "questions" in response and response["questions"]:
                maybes_section += """
                - Additional questions:
                """
                for question in response["questions"]:
                    maybes_section += f"""
                  - {question}
                    """
    
    # Generate declines section
    declines_section = ""
    if declines and include_declines:
        declines_section = """
        ## Declined Applications
        
        Unfortunately, the following lenders were unable to approve your application:
        """
        
        for lender_name, response in declines.items():
            declines_section += f"""
            ### {lender_name}
            - {response['notes']}
            """
            
            if "reasons" in response and response["reasons"]:
                declines_section += """
                - Reasons provided:
                """
                for reason in response["reasons"]:
                    declines_section += f"""
                  - {reason}
                    """
    
    # Generate next steps
    next_steps = """
    ## Next Steps
    
    I would like to schedule a call to discuss these options with you in detail. Please let me know your availability in the next few days.
    
    During our call, we can:
    1. Review the approved offers in detail
    2. Discuss any additional information needed by interested lenders
    3. Determine the best path forward based on your preferences
    
    If you have any questions in the meantime, please don't hesitate to contact me.
    """
    
    # Generate closing
    closing = """
    Thank you for choosing Arose Finance for your lending needs. I look forward to helping you secure the best possible financing solution.
    
    Best regards,
    [Broker Name]
    Arose Finance
    [Contact Information]
    """
    
    # Combine all sections
    full_template = f"{salutation}\n\n{introduction}\n\n{approvals_section}\n\n{maybes_section}\n\n{declines_section}\n\n{next_steps}\n\n{closing}"
    
    return full_template

# Get selected lenders
selected_approvals = {}
selected_maybes = {}
selected_declines = {}

for lender_name, response in lender_responses.items():
    if response["decision"] == "Yes" and st.session_state.get(f"select_approval_{lender_name}", True):
        selected_approvals[lender_name] = response
    elif response["decision"] == "Maybe" and st.session_state.get(f"select_maybe_{lender_name}", True):
        selected_maybes[lender_name] = response
    elif response["decision"] == "No" and st.session_state.get(f"select_decline_{lender_name}", False):
        selected_declines[lender_name] = response

# Email customization options
st.subheader("Email Customization")

col1, col2, col3 = st.columns(3)

with col1:
    include_approvals = st.checkbox("Include Approvals", value=True, key="include_approvals")

with col2:
    include_maybes = st.checkbox("Include Requests for More Info", value=True, key="include_maybes")

with col3:
    include_declines = st.checkbox("Include Declines", value=False, key="include_declines")

# Generate email template
client_name = f"{client_profile.get('first_name', '')} {client_profile.get('last_name', '')}"
email_template = generate_client_email(
    client_name,
    selected_approvals,
    selected_maybes,
    selected_declines,
    include_approvals,
    include_maybes,
    include_declines
)

# Display and allow editing of email template
st.subheader("Email Preview")
edited_template = st.text_area("Edit Email Template", value=email_template, height=400)

# Save template to session state
st.session_state.client_communication['email_template'] = edited_template

# Selected offers for client
selected_offers = []
for lender_name in selected_approvals.keys():
    selected_offers.append({
        "lender": lender_name,
        "decision": "Yes",
        "included_in_email": include_approvals
    })

for lender_name in selected_maybes.keys():
    selected_offers.append({
        "lender": lender_name,
        "decision": "Maybe",
        "included_in_email": include_maybes
    })

for lender_name in selected_declines.keys():
    selected_offers.append({
        "lender": lender_name,
        "decision": "No",
        "included_in_email": include_declines
    })

st.session_state.client_communication['selected_offers'] = selected_offers

# Send email button
if st.button("Send Email to Client"):
    with st.spinner("Sending email to client..."):
        # Simulate email sending
        time.sleep(2)
        
        # Record email sent
        st.session_state.client_communication['email_sent'] = True
        st.session_state.client_communication['email_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        st.success(f"✅ Email successfully sent to {client_profile.get('email', 'client')}!")
        
        # Display output
        st.subheader("Output Generated")
        st.markdown("✅ Email sent to client with terms")
        
        st.balloons()

# If email already sent, show confirmation
if st.session_state.client_communication.get('email_sent'):
    st.success(f"✅ Email was sent to client on {st.session_state.client_communication.get('email_timestamp')}")
    
    # Option to view sent email
    if st.button("View Sent Email"):
        st.info("Email Content:")
        st.markdown(st.session_state.client_communication['email_template'])

# Process Completion
st.header("Process Completion")
st.info("This completes the loan origination workflow from initial call to client communication.")

# Display workflow summary
st.subheader("Workflow Summary")

# Create a timeline of completed steps
workflow_steps = [
    "Initial Call Transcript",
    "Document Collection Form",
    "Fact-Find Completion",
    "Broker Verification",
    "Lender Matching",
    "Algorithm Learning",
    "Lender Communication",
    "Client Communication"
]

workflow_status = ["Completed"] * 8  # All steps are completed at this point

# Create a status dataframe
status_data = {
    "Step": workflow_steps,
    "Status": workflow_status
}

status_df = pd.DataFrame(status_data)

# Display as a horizontal bar chart
fig = px.timeline(
    status_df, 
    x_start=0, 
    x_end=[1] * len(workflow_steps), 
    y="Step",
    color="Status",
    color_discrete_map={"Completed": "#28a745"},
    title="Loan Origination Workflow"
)

fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    margin=dict(l=0, r=0, t=40, b=0),
    height=300,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Final message
st.success("🎉 Congratulations! You have successfully completed the entire loan origination process.")
st.info("The client has been informed of the available loan options and next steps. Follow up with the client to finalize their preferred option.") 
# Arose Finance - Loan Origination System

A comprehensive loan origination system built with Streamlit that guides users through the complete loan origination process, from application intake to final disbursement.

## Features

- **Application Intake**: Collect borrower information and loan request details
- **Document Collection**: Upload and verify required documentation
- **Credit Bureau Integration**: Retrieve and analyze credit reports
- **Financial Analysis**: Evaluate borrower's financial health and loan affordability
- **Lender Criteria Assessment**: Determine if the application meets lender requirements using a machine learning model
- **Loan Structuring**: Configure loan terms based on risk assessment
- **Approval Process**: Final review and decision making
- **Disbursement**: Process loan funding and distribution

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/arose-finance.git
   cd arose-finance
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run Home.py
   ```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Follow the workflow steps in the sidebar to complete the loan origination process

## Data Storage

This application uses Streamlit's session state to store data between pages. In a production environment, you would want to replace this with a proper database solution.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [scikit-learn](https://scikit-learn.org/) for the loan approval prediction model
- Visualizations powered by [Plotly](https://plotly.com/) and [Matplotlib](https://matplotlib.org/)
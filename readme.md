#                                        PDF Generation and Email Automation

## What does the tool do ?
This project automates the process of loading data from various sources, 
generating analysis in PDF format, and sending the PDF via email. 
The solution is built with Python and uses libraries such as matolib and pandas.

## Files
1. app.py: The main entry point that sequentially runs the scripts for data loading, analysis, and email sending.
2. load_data_from_sources_to_dfs.py: Contains logic to load data from various sources into DataFrames.
3. analysis_of_dfs_to_pdf.py: Analyzes the data from the DataFrames and generates a PDF report.
4. send_pdf_via_email.py: Sends the generated PDF report via email using configured credentials.
5. app_config.py: Loads email configuration from a .env file and stores it as environment variables.
6. requirements.txt: Contains all the Python dependencies for the project.


## Customization
- Data Loading: Modify load_data_from_sources_to_dfs.py to customize the data source (e.g., databases, CSV files, APIs).
- Analysis: Customize analysis_of_dfs_to_pdf.py to change the analysis or data visualizations.
- Email Sending: Update the send_pdf_via_email.py script to configure the recipient email, subject, and body.
- run the application using <python app/app.py> which will Load data from various sources, perform analysis and generate a PDF report and send the generated PDF via email. Please feel free running manually other files separtly which are mentioned above.

Go and work your magic ! 🪄

# # # For further information or contributions, please contact Alisa Mitchkov at alisamitchikov@gmail.com.
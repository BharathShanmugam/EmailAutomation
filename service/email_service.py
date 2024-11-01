import os
import sys

from sqlalchemy import func
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime,timezone
from sqlmodel import Session, select
from model.email_model import ExcelExtract,SentEmail,RepliedEmail,RetryEmail,ExcelStoreTable,LogEntry
from service.utlis import send_email
import pytz
import logging
import numpy as np 
from fastapi import HTTPException
from database.db import engine


# File paths for storing Excel files
REPLIED_PATH = "/home/bharath/Documents/MYEMAIL/STORE/REPLYED"  
RETRY_PATH = "/home/bharath/Documents/MYEMAIL/STORE/RETRY"
SENT_PATH = "/home/bharath/Documents/MYEMAIL/STORE/SENT"


LOG_PATH = f"/home/bharath/Documents/MYEMAIL/STORE/LOGS/{datetime.now().strftime('%Y-%m-%d')}"

# Create the log folder if it doesn't exist
os.makedirs(LOG_PATH, exist_ok=True)

# Configure logging for sent and error emails
sent_log_file = os.path.join(LOG_PATH, "sentemail.log")
error_log_file = os.path.join(LOG_PATH, "erroremail.log")

logging.basicConfig(level=logging.INFO)
sent_logger = logging.getLogger('sentemail')
sent_handler = logging.FileHandler(sent_log_file)
sent_logger.addHandler(sent_handler)

error_logger = logging.getLogger('erroremail')
error_handler = logging.FileHandler(error_log_file)
error_logger.addHandler(error_handler)



# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)





def extract_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    df = df.replace({np.nan: None})

    # Map the field names to standard names
    field_mapping = {
        "First Name": "firstname", "first name": "firstname", "First-name": "firstname", "First-Name": "firstname",
        "Last Name": "lastname", "last name": "lastname", "Last-name": "lastname", "Last-Name": "lastname",
        "Company": "company", "company": "company",
        "Company Domain": "company_domain", "Company domain": "company_domain", "company domain": "company_domain", "company Domain": "company_domain"
    }

    standardized_data = []
    for row in df.to_dict(orient='records'):
        standardized_row = {field_mapping.get(k, k): v for k, v in row.items()}
        standardized_data.append(standardized_row)

    return standardized_data

def generate_email(firstname, lastname, company, company_domain=None):
    company = company.replace(" ", "").lower()
    if company_domain:
        return f"{firstname.lower()}.{lastname.lower()}@{company_domain.lower()}"
    return f"{firstname.lower()}.{lastname.lower()}@{company}.com"

def extract_details_from_email(email):
    match = re.match(r"([^.]+)\.([^.]+)@([^.]+)\.", email)
    if match:
        return match.group(1).capitalize(), match.group(2).capitalize(), match.group(3).capitalize()
    return None, None, None

def save_extracted_data(session: Session, data):
    for row in data:
        firstname = row.get('firstname')
        lastname = row.get('lastname')
        company = row.get('company')
        email = row.get('email')
        company_domain = row.get('company_domain')

        # Populate missing fields using email details if available
        if not firstname or not lastname or not company:
            if email:
                extracted_firstname, extracted_lastname, extracted_company = extract_details_from_email(email)
                firstname = firstname or extracted_firstname
                lastname = lastname or extracted_lastname
                company = company or extracted_company

        # Generate email if missing
        if firstname and lastname and company and not email:
            email = generate_email(firstname, lastname, company, company_domain)

        # Store data in the appropriate table based on completeness
        if firstname and lastname and company and email:
            new_record = ExcelExtract(
                firstname=firstname,
                lastname=lastname,
                company=company,
                email=email,
                company_domain=company_domain
            )
            session.add(new_record)
            create_log_entry(session, "Transfer to ExcelExtract", f"Record for {firstname} {lastname} from {company} transferred to ExcelExtract")
            session.query(ExcelStoreTable).filter(
                ExcelStoreTable.firstname == firstname,
                ExcelStoreTable.lastname == lastname,
                ExcelStoreTable.company == company
            ).delete()
        else:
            incomplete_record = ExcelStoreTable(
                firstname=firstname,
                lastname=lastname,
                company=company,
                email=email,
                company_domain=company_domain
            )
            session.add(incomplete_record)

    session.commit()

def create_log_entry(session, operation: str, details: str):
    log_entry = LogEntry(operation=operation, details=details)
    session.add(log_entry)
    session.commit()
















# def extract_data_from_excel(file_path):
#     df = pd.read_excel(file_path)
#     return df.replace({np.nan: None}).to_dict(orient='records')

# def generate_email(firstname, lastname, company):
#     return f"{firstname.lower()}.{lastname.lower()}@{company.lower()}.com"

# def extract_details_from_email(email):
#     match = re.match(r"([^.]+)\.([^.]+)@([^.]+)\.", email)
#     if match:
#         return match.group(1).capitalize(), match.group(2).capitalize(), match.group(3).capitalize()
#     return None, None, None

# def save_extracted_data(session: Session, data):
#     for row in data:
#         firstname = row.get('firstname')
#         lastname = row.get('lastname')
#         email = row.get('email')
#         company = row.get('company')

#         if not firstname or not lastname or not company:
#             # Populate missing fields using email details if available
#             if email:
#                 extracted_firstname, extracted_lastname, extracted_company = extract_details_from_email(email)
#                 firstname = firstname or extracted_firstname
#                 lastname = lastname or extracted_lastname
#                 company = company or extracted_company

#         if firstname and lastname and company and not email:
#             email = generate_email(firstname, lastname, company)

#         # Determine whether to store in ExcelExtract or ExcelStoreTable
#         if firstname and lastname and email and company:
#             new_record = ExcelExtract(firstname=firstname, lastname=lastname, email=email, company=company)
#             session.add(new_record)

#             create_log_entry(
#                 session, "Transfer to ExcelExtract",
#                 f"Record for {firstname} {lastname} from {company} transferred to ExcelExtract"
#             )

#             session.query(ExcelStoreTable).filter(
#                 ExcelStoreTable.firstname == firstname,
#                 ExcelStoreTable.lastname == lastname,
#                 ExcelStoreTable.company == company
#             ).delete()
#         else:
#             incomplete_record = ExcelStoreTable(firstname=firstname, lastname=lastname, email=email, company=company)
#             session.add(incomplete_record)

#     session.commit()
    
# def create_log_entry(session, operation: str, details: str):
#     if operation is None:
#         operation = "Unknown Operation"  # Default value if None
#         print("Warning: 'operation' was None. Assigned default value.")
    
#     log_entry = LogEntry(operation=operation, details=details)
#     session.add(log_entry)
#     session.commit()
































def list_sent_emails(session: Session):
    return session.exec(select(SentEmail)).all()

def list_not_sent_emails(session: Session):
    return session.exec(select(RetryEmail)).all()

def retry_sending_emails(session: Session):
    failed_emails = session.exec(select(RetryEmail)).all()
    for email in failed_emails:
        email_sent = send_email(None, email.email, email.subject, None)
        if email_sent:
            session.add(SentEmail(email=email.email, subject=email.subject, date_sent=datetime.now(timezone.utc)))
            session.delete(email)
    session.commit()

def save_emails_to_excel(session: Session, sent=True):
    if sent:
        emails = session.exec(select(SentEmail)).all()
        filename = f"{SENT_PATH}/sentmail_{datetime.now(timezone.utc).date()}.xlsx"
    else:
        emails = session.exec(select(RetryEmail)).all()
        filename = f"{RETRY_PATH}/notsentmail_{datetime.now(timezone.utc).date()}.xlsx"
    
    df = pd.DataFrame([email.model_dump() for email in emails])
    df.to_excel(filename, index=False)
    return filename

def search_by_firstname_or_email(session: Session, query: str):
    # Search by firstname or email in all tables
    query_str = f"%{query}%"
    sent_emails = session.exec(select(SentEmail).where(SentEmail.email.like(query_str))).all()
    retry_emails = session.exec(select(RetryEmail).where(RetryEmail.email.like(query_str))).all()
    return sent_emails + retry_emails

def update_replied(session: Session, email_id: int, replied: bool):
    email = session.get(SentEmail, email_id)
    if email:
        email.replied = replied
        if replied:
            replied_record = RepliedEmail(
                email=email.email, subject=email.subject, date_sent=email.date_sent, date_replied=datetime.utcnow()
            )
            session.add(replied_record)
            session.delete(email)
        session.commit()

def save_replied_emails_to_excel(session: Session):
    replied_emails = session.exec(select(RepliedEmail)).all()
    filename = f"{REPLIED_PATH}/replied_{datetime.now(timezone.utc).date()}.xlsx"
    df = pd.DataFrame([email.model_dump() for email in replied_emails])
    df.to_excel(filename, index=False)
    return filename







import re

def send_single_email(session: Session, email: str):
    """Send a single email based on the provided email address, store result, and clean up."""
    try:
        # Convert email to lowercase for consistency
        email_lower = email.lower()

        # Attempt to fetch the record from ExcelExtract, but proceed even if not found
        record = session.exec(select(ExcelExtract).where(func.lower(ExcelExtract.email) == email_lower)).first()

        # Initialize firstname and company
        firstname = "Hiring Manager"
        company = "Company"

        # Check if record is found and extract details
        if record:
            firstname = record.firstname if record.firstname else firstname
            company = record.company if record.company else company
        else:
            # Extract firstname and company from email if record not found
            email_parts = email_lower.split('@')
            if len(email_parts) == 2:
                # Extract first name
                first_part = email_parts[0]
                # Use regex to extract alphabetic characters only before any non-alphabetic character
                match = re.match(r'([a-zA-Z]+)', first_part)
                firstname = match.group(0) if match else first_part.capitalize()

                # Extract company name
                company_part = email_parts[1].split('.')[0]  # Extract domain name as company
                if company_part == "gmail":
                    company = "your company"
                else:
                    company = company_part.capitalize()

        role = record.role if record and record.role else 'Software/Cloud Engineer'
        subject = f"Inquiry Regarding {role} Position and Future Opportunities"

        # Attempt to send the email
        email_sent = send_email(firstname, email, subject, company, role)

        if email_sent:
            # Log and store successful email in SentEmail
            sent_record = SentEmail(email=email, subject=subject, date_sent=datetime.now(timezone.utc))
            session.add(sent_record)
            sent_logger.info(f"Single email sent successfully to: {email} with subject: {subject}.")
        else:
            # Log and store failed email in RetryEmail
            retry_record = RetryEmail(email=email, subject=subject, reason="Failed to send email", date_failed=datetime.now(timezone.utc))
            session.add(retry_record)
            error_logger.error(f"Failed to send single email to: {email} with subject: {subject}.")

        # If the email was found in ExcelExtract, delete the processed record
        if record:
            session.delete(record)
            sent_logger.info(f"Deleted record for {email} from ExcelExtract after processing.")

        # Commit the transaction
        session.commit()
        return {"message": f"Email to {email} processed and {('sent' if email_sent else 'failed')}"}

    except Exception as e:
        # Rollback the session in case of an error and log it
        session.rollback()
        error_logger.error(f"Error while processing email for {email}: {str(e)}")
        return {"message": "An error occurred while processing the email."}

    finally:
        # Ensure that session is properly closed
        session.close()






def process_and_send_emails(session: Session, data: list):
    try:
        for record in data:
            email = record.email
            subject = f"Inquiry Regarding {record.role if record.role else 'Software/Cloud Engineer'} Position and Future Opportunities"
            email_sent = send_email(record.firstname, email, subject, record.company, record.role)

            if email_sent:
                sent_record = SentEmail(email=email, subject=subject, date_sent=datetime.now(timezone.utc))
                session.add(sent_record)
            else:
                retry_record = RetryEmail(email=email, subject=subject, reason="Failed to send email", date_failed=datetime.now(timezone.utc))
                session.add(retry_record)
            
            session.delete(record)

        session.commit()
    except Exception as e:
        error_logger.error(f"Error during email sending: {str(e)}")
        raise

# def process_and_send_emails(session: Session, data: list):
#     try:
#         for record in data:
#             email = record.email
#             subject = f"Inquiry Regarding {record.role if record.role else 'Software/Cloud Engineer'} Position and Future Opportunities"
#             # Send email logic
#             email_sent = send_email(record.firstname, email, subject, record.company, record.role)

#             if email_sent:
#                 # Log and store successful email
#                 sent_record = SentEmail(email=email, subject=subject, date_sent=datetime.now(timezone.utc))
#                 session.add(sent_record)
#                 sent_logger.info(f"Email sent successfully to: {email} with subject: {subject}.")
#             else:
#                 # Log and store failed email
#                 retry_record = RetryEmail(email=email, subject=subject, reason="Failed to send email", date_failed=datetime.now(timezone.utc))
#                 session.add(retry_record)
#                 error_logger.error(f"Failed to send email to: {email} with subject: {subject}.")

#             # Delete the processed record from ExcelExtract
#             session.delete(record)

#         session.commit()
#     except Exception as e:
#         error_logger.error(f"Error during email sending: {str(e)}")
#         raise





import pandas as pd


class ExcelService:
    @staticmethod
    def truncate_excel(file_path: str) -> bool:
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)

            # Clear all rows but keep the column headers
            df = df.iloc[0:0]

            # Write back the empty dataframe (with headers only) to the Excel file
            with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, index=False)

                # Get the workbook and the active sheet
                workbook = writer.book
                worksheet = workbook.active

               
                cm_to_excel_width = 8 / 2.54  # Convert cm to inches (1 inch = 2.54 cm)
                column_width = cm_to_excel_width * 10  # Approximate width in Excel units

                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter  # Get the column letter

                    # Find the maximum length of the column values
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass

                    # Set the width for the column, using max_length or the fixed width
                    worksheet.column_dimensions[column_letter].width = max(5.0, column_width)

            return True
        except Exception as e:
            print(f"Error truncating Excel file: {e}")
            return False













class EmailExtractService:
    @staticmethod
    def extract_data_from_excel(file_path: str) -> list:
        """Extract data from the provided Excel file path."""
        try:
            # Read the Excel file from the specified path
            df = pd.read_excel(file_path)
            
            # Convert DataFrame to a list of dictionaries
            data = df.to_dict(orient='records')
            return data
        except Exception as e:
            print(f"Error extracting data from Excel file at {file_path}: {e}")
            return []

    @staticmethod
    def save_extracted_data(session: Session, data: list):
        for record in data:
            # Extract fields safely, providing defaults for missing values
            firstname = record.get('firstname', '')
            lastname = record.get('lastname', '')
            company = record.get('company', '')
            email = record.get('email', '')  # Default to empty string if email is not present
            role = record.get('role', '')

            # Check for NaN and replace with empty strings
            if isinstance(company, float) and np.isnan(company):
                company = ''
            if isinstance(role, float) and np.isnan(role):
                role = ''
            if isinstance(email, float) and np.isnan(email):
                email = ''
            if isinstance(firstname, float) and np.isnan(firstname):
                firstname = ''
            if isinstance(lastname, float) and np.isnan(lastname):
                lastname = ''

            # If firstname and company are not provided, extract from email
            if not firstname and not company and email:
                email_parts = email.split('@')
                if len(email_parts) == 2:
                    first_part = email_parts[0]
                    # Extract first name using regex
                    match = re.match(r'([a-zA-Z]+)', first_part)
                    firstname = match.group(0) if match else first_part.capitalize()  # Use extracted name
                    
                    # Extract company name from the domain part
                    domain_part = email_parts[1].split('.')[0]  # Take the part before the first dot
                    if domain_part.lower() == "gmail":
                        company = "your company"  # Replace with "your company"
                    else:
                        company = domain_part.capitalize()  # Capitalize the company name
                    
                    # Extract lastname if available in the email
                    if '.' in first_part:
                        last_part = first_part.split('.')[-1]
                        lastname = last_part.capitalize()  # Capitalize the last name

            # Generate an email if it's empty
            if not email:  # If email is empty, generate one
                email = generate_email(firstname, lastname, company)

            # Log the record being saved for debugging purposes
            print(f"Saving record: {firstname}, {lastname}, {company}, {email}, {role}")

            # Create and save the entry to the ExcelExtract table
            email_entry = ExcelExtract(
                firstname=firstname,
                lastname=lastname,
                company=company,
                email=email,  # Store the generated or provided email
                role=role  # Store the role, even if it's an empty string
            )
            session.add(email_entry)

        # Commit the session to save all entries
        session.commit()





# def save_extracted_data(session: Session, data: list):
#     for record in data:
#         # Extract fields safely, providing defaults for missing values
#         firstname = record.get('firstname', '')
#         lastname = record.get('lastname', '')
#         company = record.get('company', '')
#         email = record.get('email', '')  # Default to empty string if email is not present
#         role = record.get('role', '')

#         # Check for NaN and replace with empty strings
#         if isinstance(company, float) and np.isnan(company):
#             company = ''
#         if isinstance(role, float) and np.isnan(role):
#             role = ''
#         if isinstance(email, float) and np.isnan(email):
#             email = ''
#         if isinstance(firstname, float) and np.isnan(firstname):
#             firstname = ''
#         if isinstance(lastname, float) and np.isnan(lastname):
#             lastname = ''

#         # Generate an email if it's empty
#         if not email:  # If email is empty, generate one
#             email = generate_email(firstname, lastname, company)

#         # Log the record being saved for debugging purposes
#         print(f"Saving record: {firstname}, {lastname}, {company}, {email}, {role}")

#         # Create and save the entry to the ExcelExtract table
#         email_entry = ExcelExtract(
#             firstname=firstname,
#             lastname=lastname,
#             company=company,
#             email=email,  # Store the generated or provided email
#             role=role  # Store the role, even if it's an empty string
#         )
#         session.add(email_entry)

#     # Commit the session to save all entries
#     session.commit()


# def send_single_email(session: Session, email: str):
#     """Send a single email based on the provided email address, store result, and clean up."""
#     try:
#         # Convert email to lowercase for consistency
#         email_lower = email.lower()

#         # Attempt to fetch the record from ExcelExtract, but proceed even if not found
#         record = session.exec(select(ExcelExtract).where(func.lower(ExcelExtract.email) == email_lower)).first()

#         # Generate email details (use extracted data if available, else use defaults)
#         firstname = record.firstname if record else "Hiring Manager"
#         company = record.company if record else "Company"
#         role = record.role if record.role else 'Software/Cloud Engineer'
#         subject=f"Inquiry Regarding {role} Position and Future Opportunities"

#         # Attempt to send the email
#         email_sent = send_email(firstname, email, subject, company, role)

#         if email_sent:
#             # Log and store successful email in SentEmail
#             sent_record = SentEmail(email=email, subject=subject, date_sent=datetime.now(timezone.utc))
#             session.add(sent_record)
#             sent_logger.info(f"Single email sent successfully to: {email} with subject: {subject}.")
#         else:
#             # Log and store failed email in RetryEmail
#             retry_record = RetryEmail(email=email, subject=subject, reason="Failed to send email", date_failed=datetime.now(timezone.utc))
#             session.add(retry_record)
#             error_logger.error(f"Failed to send single email to: {email} with subject: {subject}.")

#         # If the email was found in ExcelExtract, delete the processed record
#         if record:
#             session.delete(record)
#             sent_logger.info(f"Deleted record for {email} from ExcelExtract after processing.")

#         # Commit the transaction
#         session.commit()
#         return {"message": f"Email to {email} processed and {('sent' if email_sent else 'failed')}"}

#     except Exception as e:
#         # Rollback the session in case of an error and log it
#         session.rollback()
#         error_logger.error(f"Error while processing email for {email}: {str(e)}")
#         return {"message": "An error occurred while processing the email."}

#     finally:
#         # Ensure that session is properly closed
#         session.close()




















# import pandas as pd

# class ExcelService:
#     @staticmethod
#     def truncate_excel(file_path: str) -> bool:
#         try:
#             # Read the Excel file
#             df = pd.read_excel(file_path)
            
#             # Clear all rows but keep the column headers
#             df = df.iloc[0:0]
            
#             # Write back the empty dataframe (with headers only) to the Excel file
#             with pd.ExcelWriter(file_path, engine='openpyxl', mode='w') as writer:
#                 df.to_excel(writer, index=False)
            
#             return True
#         except Exception as e:
#             print(f"Error truncating Excel file: {e}")
#             return False

























# def process_and_send_single_email(session: Session, email: str):
#     try:
#         # Fetch user data by email from ExcelExtract table
#         record = session.exec(select(ExcelExtract).where(ExcelExtract.email == email)).first()

#         if not record:
#             logger.error(f"No record found for email: {email}")
#             return {"message": "Email not found in database"}

#         subject = f"Inquiry Regarding {record.role if record.role else 'Vacancies'}"

#         # Send email
#         email_sent = send_email(record.firstname, email, subject, record.company, record.role)

#         if email_sent:
#             # Log successful email
#             sent_record = SentEmail(email=email, subject=subject, date_sent=datetime.now(timezone.utc))
#             session.add(sent_record)
#             session.commit()

#             logger.info(f"Email sent successfully to: {email}")
#             return {"message": f"Email sent successfully to {email}"}
#         else:
#             # Log email to retry
#             retry_record = RetryEmail(email=email, subject=subject, reason="Failed to send email", date_failed=datetime.now(timezone.utc))
#             session.add(retry_record)
#             session.commit()

#             logger.error(f"Failed to send email to: {email}")
#             return {"message": f"Failed to send email to {email}"}

#     except Exception as e:
#         session.rollback()  # Rollback in case of any failure
#         logger.error(f"Error in processing email for {email}: {str(e)}")
#         return {"message": "Error processing email"}









# def send_single_email(session: Session, email: str):
#     """Send a single email based on the provided email address."""
#     record = session.exec(select(ExcelExtract).where(ExcelExtract.email == email)).first()
#     if not record:
#         return {"message": "No record found for the provided email."}

#     subject = f"Inquiry Regarding {record.role if record.role else 'Vacancies'}"
#     email_sent = send_email(record.firstname, email, subject, record.company, record.role)

#     if email_sent:
#         sent_record = SentEmail(email=email, subject=subject, date_sent=datetime.now(timezone.utc))
#         session.add(sent_record)
#         sent_logger.info(f"Single email sent successfully to: {email} with subject: {subject}.")
#     else:
#         retry_record = RetryEmail(email=email, subject=subject, reason="Failed to send email", date_failed=datetime.now(timezone.utc))
#         session.add(retry_record)
#         error_logger.error(f"Failed to send single email to: {email} with subject: {subject}.")

#     # Delete the processed record from ExcelExtract
#     session.delete(record)
#     session.commit()


























# def process_and_send_emails(session: Session, data: list):
#     try:
#         for record in data:
#             email = record.email
#             subject = f"Inquiry Regarding {record.role if record.role else 'Vacancies'}"
            
#             # Send email
#             email_sent = send_email(record.firstname, email, subject, record.company, record.role)

#             if email_sent:
#                 # Log successful email
#                 sent_record = SentEmail(email=email, subject=subject, date_sent=datetime.now(timezone.utc))
#                 session.add(sent_record)
#                 logger.info(f"Email sent successfully to: {email} with subject: {subject}.")
#             else:
#                 # Log email to retry
#                 retry_record = RetryEmail(email=email, subject=subject, reason="Failed to send email", date_failed=datetime.now(timezone.utc))
#                 session.add(retry_record)
#                 logger.error(f"Failed to send email to: {email} with subject: {subject}.")

#         session.commit()
#     except HTTPException as e:
#         logger.debug(f"Error updateing user: {str(e.detail)}")
#         session.rollback()
#         return e






























from fastapi import APIRouter, Depends, UploadFile,HTTPException
from sqlmodel import Session, select
from model.email_model import ExcelExtract,ExcelStoreTable
from model.email_schema import ExcelExtractResponse
from service import email_service
from database.db import get_session
import os

Send_email=APIRouter(tags=["Send_email"])
Extract_email=APIRouter(tags=["Extract_email"])
ListEmail=APIRouter(tags=["ListEmail"])
SaveExcel=APIRouter(tags=["SaveExcel"])
Update_Email=APIRouter(tags=["Update_Email"])



@Extract_email.post("/extract-data/")
async def extract_data(file: UploadFile, session: Session = Depends(get_session)):
    data = email_service.extract_data_from_excel(file.file)
    email_service.save_extracted_data(session, data)
    return {"message": "Data extracted and stored successfully"}

@Extract_email.post("/extract-data-path/")
async def extract_data_from_path(session: Session = Depends(get_session)):
    file_path = "/home/bharath/Documents/MYEMAIL/STORE/random_data.xlsx"
    data = email_service.extract_data_from_excel(file_path)
    email_service.save_extracted_data(session, data)
    return {"message": "Data extracted and stored successfully"}




# @Extract_email.post("/extract-data/")
# async def extract_data(file: UploadFile, session: Session = Depends(get_session)):
#     data = email_service.extract_data_from_excel(file.file)
#     email_service.save_extracted_data(session, data)
#     return {"message": "Data extracted and stored successfully"}

# @Extract_email.post("/extract-data-path/")
# async def extract_data_from_path(session: Session = Depends(get_session)):
#     file_path = "/home/bharath/Documents/MYEMAIL/STORE/random_data.xlsx"
#     data = email_service.extract_data_from_excel(file_path)
#     email_service.save_extracted_data(session, data)
#     return {"message": "Data extracted and stored successfully"}


# API 2: Send Emails (Sends emails based on the saved data)
@Send_email.post("/send-emails/")
async def send_emails(session: Session = Depends(get_session)):
    # Step 1: Retrieve all records from the ExcelExtract table
    data = session.exec(select(ExcelExtract)).all()
    
    # Step 2: Process the data and send emails
    email_service.process_and_send_emails(session, data)
    
    return {"message": "Emails sent successfully"}







# API 3: List All Sent Emails
@ListEmail.get("/sent-emails-list/")
def get_sent_emails(session: Session = Depends(get_session)):
    return email_service.list_sent_emails(session)

# API 4: List All Not Sent Emails
@ListEmail.get("/not-sent-emails-list/")
def get_not_sent_emails(session: Session = Depends(get_session)):
    return email_service.list_not_sent_emails(session)

# API 5: Retry Sending Not Sent Emails
@Send_email.post("/retry-emails/")
def retry_emails(session: Session = Depends(get_session)):
    email_service.retry_sending_emails(session)
    return {"message": "Retry process complete"}

# API 6: Save Sent Emails as Excel File
@SaveExcel.post("/save-sent-emails/")
def save_sent_emails(session: Session = Depends(get_session)):
    filepath = email_service.save_emails_to_excel(session, sent=True)
    return {"message": f"Sent emails saved to {filepath}"}

# API 7: Save Not Sent Emails as Excel File
@SaveExcel.post("/save-not-sent-emails/")
def save_not_sent_emails(session: Session = Depends(get_session)):
    filepath = email_service.save_emails_to_excel(session, sent=False)
    return {"message": f"Not sent emails saved to {filepath}"}

# API 8: Search by Firstname or Email
@Update_Email.get("/search/")
def search_by_name_or_email(query: str, session: Session = Depends(get_session)):
    return email_service.search_by_firstname_or_email(session, query)

# API 9: Update Record by ID
@Update_Email.put("/update-replied/{email_id}")
def update_email_replied(email_id: int, replied: bool, session: Session = Depends(get_session)):
    email_service.update_replied(session, email_id, replied)
    return {"message": f"Email {email_id} updated with replied={replied}"}

# API 10: Save Replied Emails as Excel File
@SaveExcel.post("/save-replied-emails/")
def save_replied_emails(session: Session = Depends(get_session)):
    filepath = email_service.save_replied_emails_to_excel(session)
    return {"message": f"Replied emails saved to {filepath}"}


@Send_email.post("/send-single-email/")
async def send_single_email(email: str, session: Session = Depends(get_session)):
    email_service.send_single_email(session, email)
    return {"message": f"Email to {email} processed"}





@Extract_email.get("/extracted-data/")
async def get_extracted_data(session: Session = Depends(get_session)):
    # Fetch all records from the ExcelExtract table
    extracted_data = session.exec(select(ExcelExtract)).all()
    
    # Convert the result to a list of dictionaries
    data = [record.model_dump() for record in extracted_data]
    
    return {"extracted_data": data}




excel_delete=APIRouter(tags=["Delete Excel"])

# class FilePathRequest(BaseModel):
#     file_path: str

@excel_delete.post("/truncate-excel/")
async def truncate_excel():
    file_path ="/home/bharath/Documents/MYEMAIL/STORE/random_data.xlsx"

    # Check if the file exists
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Call the service to truncate the Excel file
    success = email_service.ExcelService.truncate_excel(file_path)
    
    if success:
        return {"message": "Excel file truncated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to truncate Excel file")







































# @Extract_email.post("/extract-data/")
# async def extract_data(file: UploadFile, session: Session = Depends(get_session)):
#     data = email_service.extract_data_from_excel(file.file)
#     email_service.process_and_send_emails(session, data)
#     return {"message": "Emails processed"}

# @ListEmail.get("/sent-emails/")
# def get_sent_emails(session: Session = Depends(get_session)):
#     return email_service.list_sent_emails(session)

# @ListEmail.get("/not-sent-emails/")
# def get_not_sent_emails(session: Session = Depends(get_session)):
#     return email_service.list_not_sent_emails(session)

# @ListEmail.post("/retry-emails/")
# def retry_emails(session: Session = Depends(get_session)):
#     email_service.retry_sending_emails(session)
#     return {"message": "Retry process complete"}

# @SaveExcel.post("/save-sent-emails/")
# def save_sent_emails(session: Session = Depends(get_session)):
#     filepath = email_service.save_emails_to_excel(session, sent=True)
#     return {"message": f"Sent emails saved to {filepath}"}

# @SaveExcel.post("/save-not-sent-emails/")
# def save_not_sent_emails(session: Session = Depends(get_session)):
#     filepath = email_service.save_emails_to_excel(session, sent=False)
#     return {"message": f"Not sent emails saved to {filepath}"}

# @Update_Email.put("/update-replied/{email_id}")
# def update_email_replied(email_id: int, replied: bool, session: Session = Depends(get_session)):
#     email_service.update_replied(session, email_id, replied)
#     return {"message": f"Email {email_id} updated with replied={replied}"}

# @SaveExcel.post("/save-replied-emails/")
# def save_replied_emails(session: Session = Depends(get_session)):
#     filepath = email_service.save_replied_emails_to_excel(session)
#     return {"message": f"Replied emails saved to {filepath}"}
from fastapi import FastAPI
from datetime import datetime
import os
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from api.email_api import Extract_email,ListEmail,Update_Email,SaveExcel,Send_email,excel_delete



app=FastAPI()


def get_log_file_path():
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_dir = f'logs/{current_date}'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, 'app.log')
    return log_file_path


log_file_path = get_log_file_path()

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.StreamHandler(sys.stdout),
                        TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=7)
                    ])

logger = logging.getLogger(__name__)
LOG_PATH = f"/home/bharath/Documents/MYEMAIL/STORE/LOGS/{datetime.now().strftime('%Y-%m-%d')}"
os.makedirs(LOG_PATH, exist_ok=True)

app.include_router(Send_email)
app.include_router(Update_Email)
app.include_router(ListEmail)
app.include_router(SaveExcel)
app.include_router(Extract_email)
app.include_router(excel_delete)
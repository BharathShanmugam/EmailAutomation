import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

POSTGRES_URL=os.getenv("POSTGRES_URL")
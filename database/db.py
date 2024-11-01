from sqlmodel import SQLModel, create_engine,Session
from fastapi import FastAPI,Depends
from typing import Annotated
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

app=FastAPI()

POSTGRES_URL=os.getenv("POSTGRES_URL")

postgresql_url = POSTGRES_URL

engine = create_engine(postgresql_url, echo=True)

def create_db_and_tables(): 
  SQLModel.metadata.create_all(engine)


create_db_and_tables() 


session = Session(engine)

def get_session():
  try:
    yield session
  finally:
    session.close()


db_dependency=Annotated[Session,Depends(get_session)]

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



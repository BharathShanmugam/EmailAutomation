from sqlmodel import SQLModel, Field
from datetime import datetime,timezone
from typing import Optional

import pytz

class ExcelExtract(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: str
    lastname: str
    company: str
    email: Optional[str] = None
    company_domain: Optional[str] = None
    role: Optional[str] = None
    
class SentEmail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    subject: str
    replied: bool = False
    date_sent: datetime = Field(default_factory=lambda: datetime.now(pytz.utc))

class RetryEmail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    subject: str
    reason: Optional[str] = None
    date_failed: datetime = Field(default_factory=lambda: datetime.now(pytz.utc))

class RepliedEmail(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    subject: str
    date_sent: datetime
    date_replied: datetime = Field(default_factory=lambda: datetime.now(pytz.utc))




class ExcelStoreTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    company_domain: Optional[str] = None
    role: Optional[str] = None


class LogEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    operation: str
    details: str






























# class ExcelEmail(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True,nullable=True)
#     firstname: str
#     lastname: str
#     company: str
#     email: Optional[str]=Field(default=None,nullable=True)
#     role: Optional[str] =Field(default=None,nullable=True)
#     source:Optional[str] =Field(default=None,nullable=True)
#     sent: str = "not-sent"  # Default is "not-sent"
#     date: datetime = Field(default_factory=lambda: datetime.now(pytz.utc))
#     replied: Optional[bool] = False

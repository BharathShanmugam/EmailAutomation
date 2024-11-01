from pydantic import BaseModel,EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional

class ExcelExtractCreate(BaseModel):
    firstname: str
    lastname: str
    company: str
    email: Optional[str] = None
    role: Optional[str] = None

class SentEmailRead(BaseModel):
    id: int
    email: str
    subject: str
    replied: bool
    date_sent: datetime

class RetryEmailRead(BaseModel):
    id: int
    email: str
    subject: str
    reason: Optional[str]
    date_failed: datetime

class RepliedEmailRead(BaseModel):
    id: int
    email: str
    subject: str
    date_sent: datetime
    date_replied: datetime

    class Config:
        orm_mode = True




class EmailGenerateRequest(BaseModel):
    firstname: str
    lastname: str
    company: str

class ExcelExtractRequest(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    company: Optional[str]
    email: Optional[str]
    role: Optional[str]

class ExcelExtractResponse(BaseModel):
    message: str





class ExcelStoreData(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    company: Optional[str]
    email: Optional[str]
    role: Optional[str] = None

class ExcelExtractData(BaseModel):
    firstname: str
    lastname: str
    company: str
    email: str
    role: Optional[str] = None



class EmailDataSchema(BaseModel):
    firstname: str
    lastname: str
    company: str
    email: Optional[EmailStr] = None
    company_domain: Optional[str] = None

    @field_validator('company_domain')
    def validate_company_domain(cls, v):
        if v:
            v = v.replace(" ", "")
        return v













# from pydantic import BaseModel
# from typing import Optional
# from datetime import datetime

# class EmailCreate(BaseModel):
#     firstname: str
#     lastname: str
#     company: str
#     email: Optional[str]
#     role: Optional[str] = None
#     source: Optional[str]=None

# class EmailUpdateReply(BaseModel):
#     replied: bool

# class EmailRead(BaseModel):
#     id: int
#     firstname: str
#     lastname: str
#     company: str
#     email: str
#     role: Optional[str]
#     source: str
#     sent: str
#     date: datetime
#     replied: Optional[bool]

#     class Config:
#         orm_mode = True

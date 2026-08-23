from pydantic import BaseModel
from typing import Optional

class ComplaintInput(BaseModel):
    complaint_text: str = "The road outside my college in Prayagraj has been broken for six months."
    applicant_id: str
    language: str = "English"
    applicant_name: Optional[str] = "Citizen"
    applicant_name: Optional[str] = "Citizen"
    applicant_name: Optional[str] = "Citizen"
    applicant_name: Optional[str] = "Citizen"
    
class ComplaintResponse(BaseModel):
    status: str
    department_identified: str
    missing_info: Optional[list[str]] = None
    rti_draft_preview: Optional[str] = None

class DownloadPDFRequest(BaseModel):
    applicant_id: str
    department: str
    subject: str
    body: str

class SendOTPRequest(BaseModel):
    mobile_number: str

class VerifyOTPRequest(BaseModel):
    mobile_number: str
    otp: str

# --- Phase 2: Rights Navigator ---
class RightsInput(BaseModel):
    situation: str
    applicant_id: str
    language: str = "English"
    applicant_name: Optional[str] = "Citizen"
    applicant_name: Optional[str] = "Citizen"
    applicant_name: Optional[str] = "Citizen"
    applicant_name: Optional[str] = "Citizen"

class RightInfo(BaseModel):
    right_name: str
    description: str
    legal_basis: str

class RightsResponse(BaseModel):
    status: str
    applicable_rights: list[RightInfo]
    next_steps: str

# --- Phase 2: Scheme Eligibility ---
class ProfileInput(BaseModel):
    age: int
    gender: str
    income: str
    occupation: str
    state: str
    applicant_id: str
    language: str = "English"
    applicant_name: Optional[str] = "Citizen"
    applicant_name: Optional[str] = "Citizen"
    applicant_name: Optional[str] = "Citizen"
    applicant_name: Optional[str] = "Citizen"

class SchemeInfo(BaseModel):
    scheme_name: str
    benefits: str
    eligibility_criteria: str
    application_link: Optional[str] = None

class SchemeResponse(BaseModel):
    status: str
    eligible_schemes: list[SchemeInfo]
class AppealInput(BaseModel):
    rti_body: str
    applicant_name: str
    language: str = "English"

class ApplicationItem(BaseModel):
    id: int
    department: str
    summary: str
    draft: str

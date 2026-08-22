from pydantic import BaseModel
from typing import Optional

class ComplaintInput(BaseModel):
    complaint_text: str = "The road outside my college in Prayagraj has been broken for six months."
    applicant_id: str = "IIT2025002"
    
class ComplaintResponse(BaseModel):
    status: str
    department_identified: str
    missing_info: Optional[list[str]] = None
    rti_draft_preview: Optional[str] = None
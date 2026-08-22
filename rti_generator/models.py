from sqlalchemy import Column, Integer, String, Text
from database import Base

class RTIDocument(Base):
    __tablename__ = "rti_documents"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(String, index=True)
    department = Column(String, index=True)
    complaint_summary = Column(Text)
    generated_json = Column(Text) # Stores the drafted form data
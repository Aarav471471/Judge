from typing import Optional
from fastapi import File, UploadFile, Form, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, schemas, rag_engine
import ai_engine # Import your new AI module
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pdf_generator
import random
import os

app = FastAPI(title="RTI Auto-Drafter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=database.engine)

mock_otp_store = {}

@app.post("/auth/send-otp")
def send_otp(req: schemas.SendOTPRequest):
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    mock_otp_store[req.mobile_number] = otp
    print(f"--- MOCK SMS GATEWAY ---")
    print(f"Sending OTP {otp} to {req.mobile_number}")
    print(f"------------------------")
    return {"status": "success", "message": "OTP sent successfully (check backend console)", "dev_otp": otp}

@app.post("/auth/verify-otp")
def verify_otp(req: schemas.VerifyOTPRequest):
    stored_otp = mock_otp_store.get(req.mobile_number)
    if not stored_otp or stored_otp != req.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    # In a real app, generate a JWT token here
    # Remove OTP after verification
    del mock_otp_store[req.mobile_number]
    return {"status": "success", "token": "mock-jwt-token"}

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/generate_rti", response_model=schemas.ComplaintResponse)
async def generate_rti_draft(
    complaint_text: str = Form(...),
    applicant_id: str = Form(...),
    language: str = Form("English"),
    applicant_name: str = Form("Citizen"),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    legal_context = rag_engine.retrieve_legal_context(complaint_text)
    
    file_bytes = None
    mime_type = None
    if file:
        file_bytes = await file.read()
        mime_type = file.content_type

    ai_response = ai_engine.draft_rti_with_llm(
        complaint_text=complaint_text,
        legal_context=legal_context,
        applicant_id=applicant_id,
        language=language,
        applicant_name=applicant_name,
        file_bytes=file_bytes,
        mime_type=mime_type
    )
    
    new_doc = models.RTIDocument(
        applicant_id=applicant_id,
        department=ai_response.get("department_identified", "Unknown"),
        complaint_summary=complaint_text,
        generated_json=ai_response.get("rti_draft_preview", "")
    )
    db.add(new_doc)
    db.commit()
    
    return {
        "status": "success",
        "department_identified": ai_response.get("department_identified"),
        "missing_info": ai_response.get("missing_info", []),
        "rti_draft_preview": ai_response.get("rti_draft_preview")
    }

@app.post("/download_pdf")
def download_pdf(req: schemas.DownloadPDFRequest):
    file_path = pdf_generator.create_rti_pdf(
        draft_text=req.body, 
        applicant_id=req.applicant_id,
        department=req.department
    )
    
    return FileResponse(
        path=file_path, 
        media_type='application/pdf', 
        filename="RTI_Application.pdf"
    )

@app.post("/navigate-rights", response_model=schemas.RightsResponse)
def navigate_rights(req: schemas.RightsInput):
    ai_response = ai_engine.navigate_rights_with_llm(req.situation, req.language)
    return {
        "status": "success",
        "applicable_rights": ai_response.get("applicable_rights", []),
        "next_steps": ai_response.get("next_steps", "")
    }

@app.post("/check-schemes", response_model=schemas.SchemeResponse)
def check_schemes(req: schemas.ProfileInput):
    profile_dict = req.dict()
    language = profile_dict.pop("language", "English")
    profile_dict.pop("applicant_id", None)
    ai_response = ai_engine.check_schemes_with_llm(profile_dict, language)
    return {
        "status": "success",
        "eligible_schemes": ai_response.get("eligible_schemes", [])
    }
@app.post("/summarize-document")
async def summarize_document(file: UploadFile = File(...), language: str = Form("English")):
    contents = await file.read()
    ai_response = ai_engine.summarize_document_with_llm(contents, file.content_type, language)
    return ai_response

@app.get("/applications/{applicant_id}")
def get_applications(applicant_id: str, db: Session = Depends(get_db)):
    docs = db.query(models.RTIDocument).filter(models.RTIDocument.applicant_id == applicant_id).all()
    res = [{"id": d.id, "department": d.department, "summary": d.complaint_summary, "draft": d.generated_json} for d in docs]
    return {"status": "success", "applications": res}

@app.post("/generate_appeal")
def generate_appeal(req: schemas.AppealInput):
    ai_response = ai_engine.draft_appeal_with_llm(req.rti_body, req.applicant_name, req.language)
    return {"status": "success", "appeal_draft": ai_response.get("appeal_draft", "")}

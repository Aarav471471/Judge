from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import database, models, schemas, rag_engine
import ai_engine # Import your new AI module
from fastapi.responses import FileResponse
import pdf_generator
import os

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="RTI Auto-Drafter API")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/generate_rti", response_model=schemas.ComplaintResponse)
def generate_rti_draft(complaint: schemas.ComplaintInput, db: Session = Depends(get_db)):
    # Step 1: Retrieve context from RAG
    legal_context = rag_engine.retrieve_legal_context(complaint.complaint_text)
    
    # Step 2: Generate the draft using Gemini
    ai_response = ai_engine.draft_rti_with_llm(
        complaint_text=complaint.complaint_text,
        legal_context=legal_context,
        applicant_id=complaint.applicant_id
    )
    
    # Step 3: Save to database
    new_doc = models.RTIDocument(
        applicant_id=complaint.applicant_id,
        department=ai_response.get("department_identified", "Unknown"),
        complaint_summary=complaint.complaint_text,
        generated_json=ai_response.get("rti_draft_preview", "")
    )
    db.add(new_doc)
    db.commit()
    
    # Return the AI structured output to the frontend
    return {
        "status": "success",
        "department_identified": ai_response.get("department_identified"),
        "missing_info": ai_response.get("missing_info", []),
        "rti_draft_preview": ai_response.get("rti_draft_preview")
    }

@app.post("/download_pdf")
def download_pdf(complaint: schemas.ComplaintInput):
    # Retrieve the last generated draft for this applicant from the DB
    # (For hackathon speed, we'll just regenerate it or mock it)
    db = database.SessionLocal()
    doc = db.query(models.RTIDocument).filter(
        models.RTIDocument.applicant_id == complaint.applicant_id
    ).order_by(models.RTIDocument.id.desc()).first()
    db.close()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    file_path = pdf_generator.create_rti_pdf(
        draft_text=doc.generated_json, 
        applicant_id=doc.applicant_id,
        department=doc.department
    )
    
    return FileResponse(
        path=file_path, 
        media_type='application/pdf', 
        filename="RTI_Application.pdf"
    )   
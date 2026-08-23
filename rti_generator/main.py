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





# CivicAssist Browser Automation Endpoint
from pydantic import BaseModel
class CivicAssistRequest(BaseModel):
    applicant_name: str
    address: str
    complaint: str
    department: str = ""

def run_playwright_sync(req: CivicAssistRequest):
    from playwright.sync_api import sync_playwright
    import time
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(viewport={'width': 1280, 'height': 800})
            page = context.new_page()
            
            page.goto("https://rtionline.gov.in")
            time.sleep(2)
            
            try:
                page.click('text="Submit Request"')
                time.sleep(3)
                page.evaluate("document.querySelector('input[type=\"checkbox\"]').checked = true")
                page.evaluate("document.querySelector('input[value=\"Submit\"]').click()")
            except Exception as e:
                print("Click error:", e)
                
            time.sleep(3)
            
            overlay_html_checkpoint = f"""
            <div id="civic-assist-overlay" style="position:fixed;top:20px;right:20px;background:#1e1b4b;color:white;padding:20px;border-radius:12px;z-index:999999;box-shadow:0 10px 25px rgba(0,0,0,0.5);font-family:sans-serif;max-width:350px;border:2px solid #3b36e8;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                    <div style="background:#3b36e8;padding:8px;border-radius:50%;">🤖</div>
                    <strong style="font-size:18px;">CivicAssist AI</strong>
                </div>
                <p style="font-size:14px;line-height:1.5;margin-bottom:15px;">I have safely halted at this security checkpoint per protocol.</p>
                <div style="background:#ff9800;color:black;padding:10px;border-radius:8px;font-size:13px;font-weight:bold;">
                    ⚠️ Security Halt: Please complete the CAPTCHA/OTP on the screen and click Submit to continue.
                </div>
            </div>
            """
            
            overlay_html_final = f"""
            <div id="civic-assist-overlay-final" style="position:fixed;top:20px;right:20px;background:#1e1b4b;color:white;padding:20px;border-radius:12px;z-index:999999;box-shadow:0 10px 25px rgba(0,0,0,0.5);font-family:sans-serif;max-width:350px;border:2px solid #3b36e8;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                    <div style="background:#10b981;padding:8px;border-radius:50%;">✅</div>
                    <strong style="font-size:18px;">CivicAssist AI</strong>
                </div>
                <p style="font-size:14px;line-height:1.5;margin-bottom:15px;">I have successfully mapped and injected your details into the official portal.</p>
                <div style="background:rgba(255,255,255,0.1);padding:10px;border-radius:8px;font-size:12px;margin-bottom:15px;">
                    <strong>Applicant:</strong> {req.applicant_name}<br/>
                    <strong>Address:</strong> {req.address[:30]}...
                </div>
                <div style="background:#10b981;color:white;padding:10px;border-radius:8px;font-size:13px;font-weight:bold;">
                    ✨ Ready for submission! Review the form and click Make Payment.
                </div>
            </div>
            """
            
            escaped_complaint = req.complaint.replace('`', '').replace('$', '')
            smart_filler_js = f"""
                const inputs = document.querySelectorAll('input[type="text"]');
                for (let inp of inputs) {{
                    let n = (inp.name || '').toLowerCase();
                    let i = (inp.id || '').toLowerCase();
                    let p = (inp.placeholder || '').toLowerCase();
                    
                    // Fill Applicant Name
                    if ((n.includes('name') || i.includes('name')) && !n.includes('search') && !i.includes('search')) {{
                        inp.value = `{req.applicant_name}`;
                    }}
                    
                    // Fill Department Search Box
                    if (n.includes('search') || i.includes('search') || p.includes('public authority')) {{
                        if (`{req.department}`) {{
                            inp.value = `{req.department}`;
                            // Trigger input event to populate the autocomplete dropdown
                            inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    }}
                }}
                
                const textareas = document.querySelectorAll('textarea');
                for (let ta of textareas) {{
                    let n = (ta.name || '').toLowerCase();
                    let i = (ta.id || '').toLowerCase();
                    
                    if (n.includes('add') || i.includes('add')) {{
                        ta.value = `{req.address.replace('`', '')}`;
                    }} else if (n.includes('rti') || i.includes('rti') || n.includes('desc') || i.includes('desc') || n.includes('text') || i.includes('text')) {{
                        ta.value = `{escaped_complaint}`;
                    }}
                }}
                
                if (textareas.length === 1) {{
                    textareas[0].value = `{escaped_complaint}`;
                }} else if (textareas.length >= 2) {{
                    if (!textareas[0].value) textareas[0].value = `{req.address.replace('`', '')}`;
                    if (!textareas[textareas.length-1].value) textareas[textareas.length-1].value = `{escaped_complaint}`;
                }}
            """
            
            start_time = time.time()
            injected_final = False
            
            while time.time() - start_time < 120:
                try:
                    current_url = page.url
                    body_exists = page.evaluate("!!document.body")
                    if body_exists:
                        if "request_email_check.php" in current_url or "index.php" in current_url:
                            has_overlay = page.evaluate("!!document.getElementById('civic-assist-overlay')")
                            if not has_overlay:
                                page.evaluate(f"document.body.insertAdjacentHTML('beforeend', `{overlay_html_checkpoint}`)")
                        elif "request.php" in current_url and "emailchk=" in current_url:
                            has_final_overlay = page.evaluate("!!document.getElementById('civic-assist-overlay-final')")
                            if not has_final_overlay:
                                page.evaluate(f"document.body.insertAdjacentHTML('beforeend', `{overlay_html_final}`)")
                                page.evaluate(smart_filler_js)
                except Exception as e:
                    print('Loop Error:', e)
                time.sleep(1)
                
            browser.close()
        except Exception as e:
            print("Playwright Error:", e)

@app.post("/auto_fill_portal")
async def auto_fill_portal(req: CivicAssistRequest):
    import threading
    t = threading.Thread(target=run_playwright_sync, args=(req,))
    t.start()
    return {"status": "success", "message": "Browser automation started!"}

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

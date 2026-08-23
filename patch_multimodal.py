import re

# 1. Update ai_engine.py
ai_path = r'c:\oosc\Judge\rti_generator\ai_engine.py'
with open(ai_path, 'r', encoding='utf-8') as f:
    ai_text = f.read()

# Signature
ai_text = ai_text.replace(
    'def draft_rti_with_llm(complaint_text: str, legal_context: str, applicant_id: str, language: str = "English", applicant_name: str = "Citizen") -> dict:',
    'def draft_rti_with_llm(complaint_text: str, legal_context: str, applicant_id: str, language: str = "English", applicant_name: str = "Citizen", file_bytes: bytes = None, mime_type: str = None) -> dict:'
)

# Replace 'response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)'
# with check for file_bytes
old_call = "response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)"
new_call = """
        contents = [prompt]
        model_to_use = 'gemini-3.5-flash'
        if file_bytes and mime_type:
            doc_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
            contents = [doc_part, prompt]
            # Switch to gemini-2.5-flash if that's preferred for multimodal, but we'll try whatever works
            model_to_use = 'gemini-2.5-flash'
        response = client.models.generate_content(model=model_to_use, contents=contents)"""
ai_text = ai_text.replace(old_call, new_call)

with open(ai_path, 'w', encoding='utf-8') as f:
    f.write(ai_text)


# 2. Update main.py
main_path = r'c:\oosc\Judge\rti_generator\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    main_text = f.read()

# Need to import Optional
if 'from typing import Optional' not in main_text:
    main_text = main_text.replace('from fastapi import File,', 'from typing import Optional\nfrom fastapi import File,')

old_endpoint = """@app.post("/generate_rti", response_model=schemas.ComplaintResponse)
def generate_rti_draft(complaint: schemas.ComplaintInput, db: Session = Depends(get_db)):
    legal_context = rag_engine.retrieve_legal_context(complaint.complaint_text)
    
    ai_response = ai_engine.draft_rti_with_llm(
        complaint_text=complaint.complaint_text,
        legal_context=legal_context,
        applicant_id=complaint.applicant_id,
        language=complaint.language,
        applicant_name=complaint.applicant_name
    )
    
    new_doc = models.RTIDocument(
        applicant_id=complaint.applicant_id,
        department=ai_response.get("department_identified", "Unknown"),
        complaint_summary=complaint.complaint_text,
        generated_json=ai_response.get("rti_draft_preview", "")
    )
    db.add(new_doc)
    db.commit()
    
    return {
        "status": "success",
        "department_identified": ai_response.get("department_identified"),
        "missing_info": ai_response.get("missing_info", []),
        "rti_draft_preview": ai_response.get("rti_draft_preview")
    }"""

new_endpoint = """@app.post("/generate_rti", response_model=schemas.ComplaintResponse)
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
    }"""
main_text = main_text.replace(old_endpoint, new_endpoint)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(main_text)


# 3. Update App.jsx
app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    app_text = f.read()

# Add states
app_text = app_text.replace(
    "const [isDraftingAppeal, setIsDraftingAppeal] = useState(false);",
    "const [isDraftingAppeal, setIsDraftingAppeal] = useState(false);\n  const [attachment, setAttachment] = useState(null);\n  const attachmentInputRef = useRef(null);"
)

# Update generateRTI
old_fetch = """      const res = await fetch('http://127.0.0.1:8000/generate_rti', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ complaint_text: finalPayload, applicant_id: userMobile, language, applicant_name: applicantName })
      });"""

new_fetch = """      const formData = new FormData();
      formData.append('complaint_text', finalPayload);
      formData.append('applicant_id', userMobile);
      formData.append('language', language);
      formData.append('applicant_name', applicantName || 'Citizen');
      if (attachment) {
        formData.append('file', attachment);
      }

      const res = await fetch('http://127.0.0.1:8000/generate_rti', {
        method: 'POST',
        body: formData
      });"""
app_text = app_text.replace(old_fetch, new_fetch)

# Add attachment UI next to the mic button
old_mic_ui = """                <button 
                  onClick={toggleListening}
                  className={`p-3 rounded-full transition-all flex items-center justify-center ${isListening ? 'bg-red-100 text-red-600 animate-pulse shadow-[0_0_15px_rgba(220,38,38,0.3)]' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'}`}
                >
                  {isListening ? <Mic size={22} /> : <MicOff size={22} />}
                </button>"""

new_mic_ui = """                <button 
                  onClick={() => attachmentInputRef.current?.click()}
                  title="Attach File/Image"
                  className={`p-3 rounded-full transition-all flex items-center justify-center ${attachment ? 'bg-indigo-100 text-indigo-600' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'}`}
                >
                  <Paperclip size={22} />
                  <input 
                    type="file" 
                    className="hidden" 
                    ref={attachmentInputRef}
                    onChange={(e) => { if(e.target.files && e.target.files[0]) setAttachment(e.target.files[0]); }}
                  />
                </button>
                <button 
                  onClick={toggleListening}
                  title="Voice Input"
                  className={`p-3 rounded-full transition-all flex items-center justify-center ${isListening ? 'bg-red-100 text-red-600 animate-pulse shadow-[0_0_15px_rgba(220,38,38,0.3)]' : 'bg-slate-100 text-slate-500 hover:bg-slate-200'}`}
                >
                  {isListening ? <Mic size={22} /> : <MicOff size={22} />}
                </button>"""
app_text = app_text.replace(old_mic_ui, new_mic_ui)

# Clear attachment on start over
app_text = app_text.replace(
    "setApplicantName(''); }",
    "setApplicantName(''); setAttachment(null); }"
)

# Show attached file name
old_submit_btn = """              <button onClick={() => generateRTI()} className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-xl transition-all flex items-center justify-center gap-2 shadow-lg shadow-indigo-200 active:scale-[0.99] group mt-2">
                Draft Application <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
              </button>"""
new_submit_btn = """              {attachment && (
                <div className="text-xs font-semibold text-indigo-600 bg-indigo-50 px-3 py-1.5 rounded-lg border border-indigo-100 truncate flex items-center gap-2 mb-2">
                  <Paperclip size={14} /> Attached: {attachment.name}
                </div>
              )}
              <button onClick={() => generateRTI()} className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-4 rounded-xl transition-all flex items-center justify-center gap-2 shadow-lg shadow-indigo-200 active:scale-[0.99] group mt-2">
                Draft Application <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
              </button>"""
app_text = app_text.replace(old_submit_btn, new_submit_btn)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_text)

print("Multimodal attachments implemented!")

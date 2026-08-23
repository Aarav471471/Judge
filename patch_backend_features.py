import os

# --- 1. Schemas ---
schemas_path = r'c:\oosc\Judge\rti_generator\schemas.py'
with open(schemas_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_schemas = """
class AppealInput(BaseModel):
    rti_body: str
    applicant_name: str
    language: str = "English"

class ApplicationItem(BaseModel):
    id: int
    department: str
    summary: str
    draft: str
"""
text += new_schemas
with open(schemas_path, 'w', encoding='utf-8') as f:
    f.write(text)

# --- 2. AI Engine ---
ai_path = r'c:\oosc\Judge\rti_generator\ai_engine.py'
with open(ai_path, 'r', encoding='utf-8') as f:
    ai_text = f.read()

new_ai = """
def draft_appeal_with_llm(rti_body: str, applicant_name: str, language: str = "English") -> dict:
    my_api_key = os.getenv("GEMINI_API_KEY")
    if not my_api_key: return {"appeal_draft": "API Key Missing"}

    client = genai.Client(api_key=my_api_key, vertexai=False)
    prompt = f'''
    You are an expert Indian legal assistant.
    A citizen drafted this RTI 30 days ago, but the department ignored it.
    
    Original RTI:
    {rti_body}
    
    Task:
    Draft a "First Appeal" under Section 19(1) of the RTI Act, 2005. 
    Address it to the "First Appellate Authority".
    Express dissatisfaction that the CPIO/PIO failed to provide information within 30 days.
    Make it formal, legal, and demanding action. Include the applicant's name at the bottom.
    Applicant Name: {applicant_name}
    
    CRITICAL: Translate the final appeal into {language}.
    
    You MUST output a valid JSON object matching exactly this structure:
    {{
        "appeal_draft": "Full text of the First Appeal..."
    }}
    '''
    try:
        response = client.models.generate_content(model='gemini-3.5-flash', contents=prompt)
        raw_response = response.text.strip()
        if raw_response.startswith("```json"): raw_response = raw_response[7:-3]
        elif raw_response.startswith("```"): raw_response = raw_response[3:-3]
        import json
        return json.loads(raw_response)
    except Exception as e:
        return {"appeal_draft": f"Failed: {e}"}
"""
ai_text += new_ai
with open(ai_path, 'w', encoding='utf-8') as f:
    f.write(ai_text)

# --- 3. Main.py ---
main_path = r'c:\oosc\Judge\rti_generator\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    main_text = f.read()

new_main = """
@app.get("/applications/{applicant_id}")
def get_applications(applicant_id: str, db: Session = Depends(get_db)):
    docs = db.query(models.RTIDocument).filter(models.RTIDocument.applicant_id == applicant_id).all()
    res = [{"id": d.id, "department": d.department, "summary": d.complaint_summary, "draft": d.generated_json} for d in docs]
    return {"status": "success", "applications": res}

@app.post("/generate_appeal")
def generate_appeal(req: schemas.AppealInput):
    ai_response = ai_engine.draft_appeal_with_llm(req.rti_body, req.applicant_name, req.language)
    return {"status": "success", "appeal_draft": ai_response.get("appeal_draft", "")}
"""
main_text += new_main
with open(main_path, 'w', encoding='utf-8') as f:
    f.write(main_text)

print("Backend features patched!")

import re
import os

# --- 1. Update schemas.py ---
schemas_path = r'c:\oosc\Judge\rti_generator\schemas.py'
with open(schemas_path, 'r', encoding='utf-8') as f:
    schemas_text = f.read()

schemas_text = schemas_text.replace(
    'applicant_id: str\n    language: str = "English"',
    'applicant_id: str\n    language: str = "English"\n    applicant_name: Optional[str] = "Citizen"'
)

with open(schemas_path, 'w', encoding='utf-8') as f:
    f.write(schemas_text)

# --- 2. Update ai_engine.py ---
ai_path = r'c:\oosc\Judge\rti_generator\ai_engine.py'
with open(ai_path, 'r', encoding='utf-8') as f:
    ai_text = f.read()

ai_text = ai_text.replace(
    'def draft_rti_with_llm(complaint_text: str, legal_context: str, applicant_id: str, language: str = "English") -> dict:',
    'def draft_rti_with_llm(complaint_text: str, legal_context: str, applicant_id: str, language: str = "English", applicant_name: str = "Citizen") -> dict:'
)

# Update the prompt inside ai_engine.py
old_prompt = """    User Complaint: "{complaint_text}"
    Applicant ID: {applicant_id}
    Legal Context Context: "{legal_context}"
    
    Task:"""

new_prompt = """    User Complaint: "{complaint_text}"
    Applicant ID: {applicant_id}
    Applicant Name: {applicant_name}
    Legal Context: "{legal_context}"
    
    Task:
    - If the user provided a "Location Context" in the complaint, use that location as the "Address of Applicant" at the bottom of the RTI.
    - Replace placeholders like [Name of Applicant] with the actual Applicant Name provided above."""

ai_text = ai_text.replace(old_prompt, new_prompt)

# Tell the AI to insert the actual name and address instead of leaving placeholders
ai_text = ai_text.replace(
    'Draft a formal RTI application based on the complaint. Address it to the "Public Information Officer" (PIO) of the identified department. Format the application clearly.',
    'Draft a formal RTI application based on the complaint. Address it to the "Public Information Officer" (PIO) of the identified department. Format the application clearly. MUST fill the Applicant Name and Address at the bottom.'
)

with open(ai_path, 'w', encoding='utf-8') as f:
    f.write(ai_text)

# --- 3. Update main.py ---
main_path = r'c:\oosc\Judge\rti_generator\main.py'
with open(main_path, 'r', encoding='utf-8') as f:
    main_text = f.read()

main_text = main_text.replace(
    'applicant_id=complaint.applicant_id,\n        language=complaint.language\n    )',
    'applicant_id=complaint.applicant_id,\n        language=complaint.language,\n        applicant_name=complaint.applicant_name\n    )'
)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(main_text)

# --- 4. Update App.jsx ---
app_path = r'c:\oosc\Judge\rti-frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    app_text = f.read()

app_text = app_text.replace(
    'body: JSON.stringify({ complaint_text: finalPayload, applicant_id: userMobile, language })',
    'body: JSON.stringify({ complaint_text: finalPayload, applicant_id: userMobile, language, applicant_name: applicantName })'
)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_text)

print("Backend and Frontend updated to pass and process applicant name and address.")

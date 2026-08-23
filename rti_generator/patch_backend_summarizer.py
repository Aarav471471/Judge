import os

# Patch ai_engine.py
with open(r'c:\oosc\Judge\rti_generator\ai_engine.py', 'r', encoding='utf-8') as f:
    ai_content = f.read()

if 'from google.genai import types' not in ai_content:
    ai_content = ai_content.replace('from google import genai', 'from google import genai\nfrom google.genai import types')

new_function = """
def summarize_document_with_llm(file_bytes: bytes, mime_type: str, language: str = "English") -> dict:
    my_api_key = os.getenv("GEMINI_API_KEY")
    if not my_api_key:
        return {"document_type": "Error", "summary": "API Key Missing", "action_required": ""}

    client = genai.Client(api_key=my_api_key, vertexai=False)
    
    prompt = f\"\"\"
    You are an expert Indian legal assistant. 
    Analyze the attached government document/paper/image.
    Provide a clear, structured summary of what this document is, its main points, and what action (if any) the citizen needs to take.
    
    CRITICAL: You MUST provide your ENTIRE response in {language}.
    
    Output a valid JSON object matching exactly this structure:
    {{
        "document_type": "e.g., Notice, FIR, Circular (in {language})",
        "summary": "Detailed summary (in {language})",
        "action_required": "What the citizen needs to do (in {language})"
    }}
    \"\"\"
    
    try:
        doc_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[doc_part, prompt]
        )
        raw_response = response.text.strip()
        if raw_response.startswith("```json"): raw_response = raw_response[7:-3]
        elif raw_response.startswith("```"): raw_response = raw_response[3:-3]
        import json
        return json.loads(raw_response)
    except Exception as e:
        print(f"Error in summarize_document_with_llm: {e}")
        return {"document_type": "Error", "summary": f"Failed to analyze: {str(e)}", "action_required": ""}
"""

if 'summarize_document_with_llm' not in ai_content:
    with open(r'c:\oosc\Judge\rti_generator\ai_engine.py', 'a', encoding='utf-8') as f:
        f.write(new_function)
        
# Patch main.py
with open(r'c:\oosc\Judge\rti_generator\main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

if 'from fastapi import FastAPI, HTTPException, Depends' in main_content:
    main_content = main_content.replace(
        'from fastapi import FastAPI, HTTPException, Depends', 
        'from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Form'
    )
elif 'from fastapi import' in main_content and 'UploadFile' not in main_content:
    main_content = main_content.replace('from fastapi import ', 'from fastapi import File, UploadFile, Form, ')

main_endpoint = """
@app.post("/summarize-document")
async def summarize_document(file: UploadFile = File(...), language: str = Form("English")):
    contents = await file.read()
    ai_response = ai_engine.summarize_document_with_llm(contents, file.content_type, language)
    return ai_response
"""

if '/summarize-document' not in main_content:
    with open(r'c:\oosc\Judge\rti_generator\main.py', 'w', encoding='utf-8') as f:
        f.write(main_content + main_endpoint)
        
print("Backend patched")

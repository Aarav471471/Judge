from google.genai import types
from google import genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def draft_rti_with_llm(complaint_text: str, legal_context: str, applicant_id: str, language: str = "English", applicant_name: str = "Citizen", file_bytes: bytes = None, mime_type: str = None) -> dict:
    """Passes the complaint and RAG context to Gemini to draft the RTI."""
    my_api_key = os.getenv("GEMINI_API_KEY")
    if not my_api_key:
        print("Error: GEMINI_API_KEY is not set in the .env file.")
        return {
            "department_identified": "Configuration Error",
            "missing_info": [],
            "rti_draft_preview": "Server configuration error: Missing API Key."
        }

    client = genai.Client(api_key=my_api_key, vertexai=False)
    
    prompt = f"""
    You are an expert Indian legal assistant specializing in the Right to Information (RTI) Act, 2005.
    
    User Complaint: "{complaint_text}"
    Applicant ID: {applicant_id}
    Applicant Name: {applicant_name}
    Legal Context: "{legal_context}"
    
    Task:
    - If the user provided a "Location Context" in the complaint, use that location as the "Address of Applicant" at the bottom of the RTI.
    - Replace placeholders like [Name of Applicant] with the actual Applicant Name provided above.
    1. Identify the specific government department responsible for this issue.
    2. Identify ONLY highly critical missing facts (like exact street name or date). Do NOT ask for administrative zones, citizenship declarations, or prior complaint histories. Assume the user is an Indian citizen. If the core facts (who, what, where, when) are present, output an empty list [] for missing_info.
    3. Draft a formal RTI application based on the complaint. Address it to the "Public Information Officer" (PIO) of the identified department. Format the application clearly. MUST fill the Applicant Name and Address at the bottom. MUST fill the Applicant Name and Address at the bottom. MUST fill the Applicant Name and Address at the bottom. MUST fill the Applicant Name and Address at the bottom.
    
    CRITICAL: Translate your responses into {language}. The `missing_info` questions and `department_identified` must be in {language}. The `rti_draft_preview` should also be translated into {language} unless it's a formal English request.
    
    You MUST output a valid JSON object matching exactly this structure:
    {{
        "department_identified": "Name of Department",
        "missing_info": ["List", "of", "missing", "details"],
        "rti_draft_preview": "Full text of the drafted RTI application..."
    }}
    """
    
    try:
        
        contents = [prompt]
        model_to_use = 'gemini-3.5-flash'
        if file_bytes and mime_type:
            doc_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
            contents = [doc_part, prompt]
            # Switch to gemini-2.5-flash if that's preferred for multimodal, but we'll try whatever works
            model_to_use = 'gemini-2.5-flash'
        response = client.models.generate_content(model=model_to_use, contents=contents)
        raw_response = response.text.strip()
        if raw_response.startswith("```json"): raw_response = raw_response[7:-3]
        elif raw_response.startswith("```"): raw_response = raw_response[3:-3]
        return json.loads(raw_response)
    except Exception as e:
        print(f"API Connection Error: {e}")
        return {"department_identified": "Connection Error", "missing_info": [], "rti_draft_preview": f"Failed to connect: {e}"}

def navigate_rights_with_llm(situation: str, language: str = "English") -> dict:
    my_api_key = os.getenv("GEMINI_API_KEY")
    if not my_api_key:
        return {"applicable_rights": [], "next_steps": "Error: Missing API Key"}

    client = genai.Client(api_key=my_api_key, vertexai=False)
    
    prompt = f"""
    You are an expert Indian legal assistant. A citizen is facing the following situation:
    "{situation}"
    
    Task:
    Identify 2-3 specific legal or constitutional rights the citizen has under Indian law relevant to this situation.
    Provide a brief description of the right and its legal basis (e.g., Article 21, specific Act).
    Also provide a brief 1-sentence recommended next step.
    
    CRITICAL: You must provide all descriptions, right names, and next steps in {language}.

    You MUST output a valid JSON object matching exactly this structure:
    {{
        "applicable_rights": [
            {{
                "right_name": "Name of the Right",
                "description": "Brief description of how it applies here.",
                "legal_basis": "The specific law/Act/Constitutional Article"
            }}
        ],
        "next_steps": "A single sentence recommending the next action."
    }}
    """
    
    try:
        
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        raw_response = response.text.strip()
        if raw_response.startswith("```json"): raw_response = raw_response[7:-3]
        elif raw_response.startswith("```"): raw_response = raw_response[3:-3]
        return json.loads(raw_response)
    except Exception as e:
        print(f"Error in navigate_rights_with_llm: {e}")
        return {"applicable_rights": [], "next_steps": "Failed to analyze rights."}

def check_schemes_with_llm(profile: dict, language: str = "English") -> dict:
    my_api_key = os.getenv("GEMINI_API_KEY")
    if not my_api_key:
        return {"eligible_schemes": []}

    client = genai.Client(api_key=my_api_key, vertexai=False)
    
    prompt = f"""
    You are an expert on Indian government welfare schemes. 
    A citizen has the following profile:
    {json.dumps(profile, indent=2)}
    
    Task:
    Identify 2-3 specific central or state government schemes they are likely eligible for based on this profile.
    For each, provide the scheme name, a brief description of benefits, eligibility criteria that matched, and a general link/portal to apply.
    
    CRITICAL: Provide all responses in {language}.

    You MUST output a valid JSON object matching exactly this structure:
    {{
        "eligible_schemes": [
            {{
                "scheme_name": "Name of Scheme",
                "benefits": "Brief description of benefits.",
                "eligibility_criteria": "Why they qualify.",
                "application_link": "URL or instruction"
            }}
        ]
    }}
    """
    
    try:
        
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        raw_response = response.text.strip()
        if raw_response.startswith("```json"): raw_response = raw_response[7:-3]
        elif raw_response.startswith("```"): raw_response = raw_response[3:-3]
        return json.loads(raw_response)
    except Exception as e:
        print(f"Error in check_schemes_with_llm: {e}")
        return {"eligible_schemes": []}
def summarize_document_with_llm(file_bytes: bytes, mime_type: str, language: str = "English") -> dict:
    my_api_key = os.getenv("GEMINI_API_KEY")
    if not my_api_key:
        return {"document_type": "Error", "summary": "API Key Missing", "action_required": ""}

    client = genai.Client(api_key=my_api_key, vertexai=False)
    
    prompt = f"""
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
    """
    
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
        
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        raw_response = response.text.strip()
        if raw_response.startswith("```json"): raw_response = raw_response[7:-3]
        elif raw_response.startswith("```"): raw_response = raw_response[3:-3]
        import json
        return json.loads(raw_response)
    except Exception as e:
        return {"appeal_draft": f"Failed: {e}"}

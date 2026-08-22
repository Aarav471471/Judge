from google import genai
import json
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def draft_rti_with_llm(complaint_text: str, legal_context: str, applicant_id: str) -> dict:
    """Passes the complaint and RAG context to Gemini to draft the RTI."""
    
    # 1. Pull the API key securely from the .env file
    my_api_key = os.getenv("GEMINI_API_KEY")
    
    # Quick safeguard if the .env file is missing
    if not my_api_key:
        print("Error: GEMINI_API_KEY is not set in the .env file.")
        return {
            "department_identified": "Configuration Error",
            "missing_info": [],
            "rti_draft_preview": "Server configuration error: Missing API Key."
        }

    # 2. Force AI Studio mode (This is your ONLY client initialization)
    client = genai.Client(
        api_key=my_api_key,
        vertexai=False 
    )
    
    prompt = f"""
    You are an expert Indian legal assistant specializing in the Right to Information (RTI) Act, 2005.
    
    User Complaint: "{complaint_text}"
    Applicant ID: {applicant_id}
    Legal Context Context: "{legal_context}"
    
    Task:
    1. Identify the specific government department responsible for this issue.
    2. Identify ONLY highly critical missing facts (like exact street name or date). Do NOT ask for administrative zones, citizenship declarations, or prior complaint histories. Assume the user is an Indian citizen. If the core facts (who, what, where, when) are present, output an empty list [] for missing_info.
    3. Draft a formal RTI application based on the complaint. Address it to the "Public Information Officer" (PIO) of the identified department. Format the application clearly.
    
    You MUST output a valid JSON object matching exactly this structure:
    {{
        "department_identified": "Name of Department",
        "missing_info": ["List", "of", "missing", "details"],
        "rti_draft_preview": "Full text of the drafted RTI application..."
    }}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt
        )
        
        raw_response = response.text.strip()
        if raw_response.startswith("```json"):
            raw_response = raw_response[7:-3]
        elif raw_response.startswith("```"):
            raw_response = raw_response[3:-3]
            
        parsed_json = json.loads(raw_response)
        return parsed_json
        
    except json.JSONDecodeError:
        print("Failed to parse JSON from AI response.")
        return {
            "department_identified": "Error parsing department",
            "missing_info": [],
            "rti_draft_preview": "Error drafting document. Please try again."
        }
    except Exception as e:
        print(f"API Connection Error: {e}")
        return {
            "department_identified": "Connection Error",
            "missing_info": [],
            "rti_draft_preview": f"Failed to connect: {e}"
        }
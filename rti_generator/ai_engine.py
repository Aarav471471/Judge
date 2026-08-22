from google import genai
import json

# The SDK automatically picks up the GEMINI_API_KEY environment variable
client = genai.Client()

def draft_rti_with_llm(complaint_text: str, legal_context: str, applicant_id: str) -> dict:
    """Passes the complaint and RAG context to Gemini to draft the RTI."""
    
    prompt = f"""
    You are an expert Indian legal assistant specializing in the Right to Information (RTI) Act, 2005.
    
    User Complaint: "{complaint_text}"
    Applicant ID: {applicant_id}
    Legal Context Context: "{legal_context}"
    
    Task:
    1. Identify the specific government department responsible for this issue.
    2. Identify what specific facts are missing (e.g., exact street name, date of incident) that the user needs to provide.
    3. Draft a formal RTI application based on the complaint. Address it to the "Public Information Officer" (PIO) of the identified department. Format the application clearly.
    
    You MUST output a valid JSON object matching exactly this structure:
    {{
        "department_identified": "Name of Department",
        "missing_info": ["List", "of", "missing", "details"],
        "rti_draft_preview": "Full text of the drafted RTI application..."
    }}
    """
    
    # Using Gemini 3.5 Flash for high speed and accuracy
    interaction = client.interactions.create(
        model="gemini-3.5-flash",
        input=prompt
    )
    
    # Strip markdown formatting in case the LLM outputs ```json
    raw_response = interaction.output_text.strip()
    if raw_response.startswith("```json"):
        raw_response = raw_response[7:-3]
        
    try:
        parsed_json = json.loads(raw_response)
        return parsed_json
    except json.JSONDecodeError:
        # Fallback in case of parsing failure
        return {
            "department_identified": "Error parsing department",
            "missing_info": [],
            "rti_draft_preview": "Error drafting document. Please try again."
        }
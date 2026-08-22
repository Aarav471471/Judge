from google import genai
import json

client = genai.Client()

# 1. Setup Mock Data for the Test
test_complaint = "The streetlights outside the IIIT campus have been completely broken for two months and the municipal corporation ignores my calls."
test_applicant_id = "IIT2025002"
test_legal_context = "Under Section 6(1) of the Right to Information Act, 2005, citizens can request information from public authorities. The Municipal Corporation is a public authority responsible for civic amenities including street lighting."

# 2. The Exact Prompt from our AI Engine
prompt = f"""
You are an expert Indian legal assistant specializing in the Right to Information (RTI) Act, 2005.

User Complaint: "{test_complaint}"
Applicant ID: {test_applicant_id}
Legal Context Context: "{test_legal_context}"

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

print("Sending RTI prompt to Gemini...")

try:
    # 3. Call the API
    response = client.models.generate_content(
        model='gemini-3.5-flash', 
        contents=prompt
    )
    
    # 4. Clean markdown and parse the JSON output
    raw_response = response.text.strip()
    if raw_response.startswith("```json"):
        raw_response = raw_response[7:-3]
    elif raw_response.startswith("```"):
        raw_response = raw_response[3:-3]
        
    parsed_json = json.loads(raw_response)
    
    print("\n--- TEST SUCCESSFUL! ---")
    print(f"\n1. Identified Department: {parsed_json.get('department_identified')}")
    print(f"\n2. Missing Info Flagged: {parsed_json.get('missing_info')}")
    print(f"\n3. Generated RTI Draft Preview:\n\n{parsed_json.get('rti_draft_preview')}")

except json.JSONDecodeError:
    print("\nTest Failed: The model did not output valid JSON.")
    print("Raw output was:\n", response.text)
except Exception as e:
    print(f"\nTest Failed: {e}")
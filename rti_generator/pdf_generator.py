from fpdf import FPDF
import os

def create_rti_pdf(draft_text: str, applicant_id: str, department: str) -> str:
    """Generates a formatted PDF and returns the file path."""
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    
    # Set margins and font
    pdf.set_margins(left=20, top=20, right=20)
    pdf.set_font("Helvetica", style="B", size=16)
    
    # Title
    pdf.cell(0, 10, "Right to Information (RTI) Application", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    # Sanitize department string just in case
    safe_dept = department.replace("₹", "Rs.").encode('latin-1', 'ignore').decode('latin-1')
    
    # Metadata Header
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Applicant ID: {applicant_id}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"To: {safe_dept}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Main Body Text
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", size=12)
    
    # --- TEXT SANITIZATION ---
    # 1. Replace Rupee symbol with "Rs."
    safe_text = draft_text.replace("₹", "Rs.")
    # 2. Flatten smart quotes to standard quotes (common AI characters that crash fpdf)
    safe_text = safe_text.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    # 3. Strip any remaining unsupported Unicode characters completely
    safe_text = safe_text.encode('latin-1', 'ignore').decode('latin-1')
    
    # Generate the text block using the sanitized string
    pdf.multi_cell(0, 8, safe_text)
    
    # Ensure the outputs directory exists
    os.makedirs("outputs", exist_ok=True)
    file_path = f"outputs/RTI_{applicant_id}.pdf"
    
    pdf.output(file_path)
    return file_path
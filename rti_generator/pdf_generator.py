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
    
    # Metadata Header
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Applicant ID: {applicant_id}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"To: {department}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    
    # Main Body Text
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 8, draft_text)
    
    # Ensure the outputs directory exists
    os.makedirs("outputs", exist_ok=True)
    file_path = f"outputs/RTI_{applicant_id}.pdf"
    
    pdf.output(file_path)
    return file_path
from fpdf import FPDF

def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    
    # Title
    pdf.cell(200, 10, txt="Event Plan & Logistics", ln=1, align="C")
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    content = [
        "Event Venue: City Convention Hall",
        "Catering Vendor: GreenLeaf Catering",
        "Guest Count: 200",
        "Transport: Airport shuttle buses arranged",
        "Keynote Speaker: John Matthews",
    ]
    
    for line in content:
        pdf.cell(200, 10, txt=line, ln=1)
        
    pdf.output("data/event_plan.pdf")
    print("PDF generated successfully at data/event_plan.pdf")

if __name__ == "__main__":
    create_pdf()

import fitz

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from any PDF file using PyMuPDF.
    """
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text("text")
    return text.strip()

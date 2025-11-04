# services/text_extractor.py
import fitz
from docx import Document
import pandas as pd
import os

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from any PDF file using PyMuPDF.
    """
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text("text")
    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text from a DOCX (Microsoft Word) file.
    """
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs).strip()

def extract_text_from_txt(file_path: str) -> str:
    """
    Reads plain text files.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def extract_text_from_csv(file_path: str) -> str:
    """
    Converts CSV content into a readable text table.
    """
    df = pd.read_csv(file_path)
    return df.to_string(index=False)

def extract_text(file_path: str) -> str:
    """
    Automatically detect file type and extract text accordingly.
    Supports PDF, DOCX, TXT and CSV.
    """
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".csv":
        return extract_text_from_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

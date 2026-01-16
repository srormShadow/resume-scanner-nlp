import pdfplumber
from docx import Document
import os

class UnsupportedFileFormatError(Exception):
    pass

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.strip()

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return " ".join([para.text for para in doc.paragraphs])

def extract_text(file_path):

    _, ext = os.path.splitext(file_path)

    ext = ext.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    elif ext == ".docx":
        return extract_text_from_docx(file_path)

    else:
        raise UnsupportedFileFormatError("Unsupported file format")

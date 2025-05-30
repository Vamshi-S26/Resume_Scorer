import os
import docx2txt
from PyPDF2 import PdfReader

def read_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"PDF Read Error: {e}")
    return text

def read_docx(file_path):
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        print(f"DOCX Read Error: {e}")
        return ""

def read_txt(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"TXT Read Error: {e}")
        return ""

def read_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return read_pdf(file_path)
    elif ext == '.docx':
        return read_docx(file_path)
    elif ext == '.txt':
        return read_txt(file_path)
    else:
        print(f"Unsupported file type: {ext}")
        return ""

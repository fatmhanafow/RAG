# backend/loader.py
import pdfplumber
import re

def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def clean_text(txt):
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt

def chunk_text(text, chunk_size=400, overlap=100):
    """
    chunk_size / overlap in tokens approximation: We'll treat token ~ word.
    chunk_size default 400 words (approx ~300-500 tokens depending)
    """
    words = text.split()
    chunks = []
    i = 0
    idn = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
        idn += 1
    return chunks

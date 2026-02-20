# backend/loader.py
import pdfplumber
import re
import fitz  # pymupdf
from PIL import Image
import pytesseract
import io
import os

TESSERACT_DIR = r'D:\OCR'
TESSERACT_EXE = os.path.join(TESSERACT_DIR, 'tesseract.exe')
TESSDATA_DIR = os.path.join(TESSERACT_DIR, 'tessdata')
FAS_PATH = os.path.join(TESSDATA_DIR, 'fas.traineddata')
ENG_PATH = os.path.join(TESSDATA_DIR, 'eng.traineddata')
pytesseract.pytesseract.tesseract_cmd = r'D:\OCR\tesseract.exe'

def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf(path):
    text_pages = []
    with fitz.open(path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            page_text = page.get_text().strip()
            
            if page_text:
                text_pages.append(page_text)
            else:
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # OCR با زبان فارسی
                ocr_text = pytesseract.image_to_string(img, lang='fas')
                text_pages.append(ocr_text.strip())
    
    return "\n".join(text_pages)
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

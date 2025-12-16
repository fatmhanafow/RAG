# backend/main.py
from fastapi import FastAPI, UploadFile, File, Form
from loader import load_txt, load_pdf, clean_text, chunk_text
from embedder import Embedder
from weaviate_client import LocalVectorDB
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

app = FastAPI(title="RAG PoC CPU")

# -------------------------
# Initialize Embedder + Local DB
# -------------------------
embedder = Embedder()
vector_db = LocalVectorDB(dim=1024)

# -------------------------
# Startup event (optional)
# -------------------------
@app.on_event("startup")
def startup_event():
    # اگر میخوای schema خاص بسازی، اینجا بزار
    print("RAG PoC CPU started. Embedder + LocalVectorDB ready.")

# -------------------------
# Upload endpoint
# -------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), chunk_size: int = 400, overlap: int = 100):
    # ذخیره موقت
    tmp = f"/tmp/{file.filename}"
    content = await file.read()
    os.makedirs("/tmp", exist_ok=True)
    with open(tmp, "wb") as f:
        f.write(content)

    ext = file.filename.split(".")[-1].lower()
    if ext == "pdf":
        text = load_pdf(tmp)
    else:
        text = load_txt(tmp)

    text = clean_text(text)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    # embedding
    vectors = embedder.encode(chunks)

    # اضافه به LocalVectorDB
    docs = []
    for i, c in enumerate(chunks):
        docs.append({"id": f"{file.filename}-{i}", "text": c, "vector": vectors[i], "source": file.filename})
    vector_db.add(np.array(vectors), [d["text"] for d in docs])

    return {"status": "ok", "chunks_indexed": len(docs)}

# -------------------------
# Search endpoint
# -------------------------
@app.post("/search")
async def search(q: str = Form(...), k: int = Form(5)):
    q_vec = embedder.encode([f"Represent this sentence for searching relevant passages: {q}"])[0]
    hits = vector_db.query(np.array([q_vec]), top_k=k)
    return {"query": q, "results": [{"text": t, "score": float(s)} for t, s in hits]}

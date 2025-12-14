from fastapi import FastAPI, UploadFile, File, Form
from backend.loader import load_txt, load_pdf, clean_text, chunk_text
from backend.embedder import embed_texts
from backend.weaviate_client import create_schema, index_chunks, query_top_k

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="RAG PoC")

@app.on_event("startup")
def startup_event():
    create_schema()

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    chunk_size: int = 400,
    overlap: int = 100
):
    ext = file.filename.split(".")[-1].lower()
    content = await file.read()

    tmp = f"/tmp/{file.filename}"
    with open(tmp, "wb") as f:
        f.write(content)

    if ext == "pdf":
        text = load_pdf(tmp)
    else:
        text = load_txt(tmp)

    text = clean_text(text)
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    vectors = embed_texts(chunks)

    docs = [
        {
            "id": f"{file.filename}-{i}",
            "text": c,
            "vector": vectors[i],
            "source": file.filename,
        }
        for i, c in enumerate(chunks)
    ]

    index_chunks(docs)
    return {"status": "ok", "chunks_indexed": len(docs)}

@app.post("/search")
async def search(q: str = Form(...), k: int = Form(5)):
    q_vec = embed_texts([q])[0]
    hits = query_top_k(q_vec, k=k)
    return {"query": q, "results": hits}

from fastapi import FastAPI, UploadFile, File, Form
from loader import load_txt, load_pdf, clean_text, chunk_text
from embedder import Embedder
from weaviate_client import WeaviateVectorDB
import os

app = FastAPI(title="RAG PoC – Retrieval Only")

embedder = Embedder()
vector_db = None 


@app.on_event("startup")
def startup():
    global vector_db
    vector_db = WeaviateVectorDB() 
    vector_db.create_schema()   
    print("Weaviate schema ready.")
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    chunk_size: int = 400,
    overlap: int = 100
):
    tmp_path = f"/tmp/{file.filename}"
    os.makedirs("/tmp", exist_ok=True)

    with open(tmp_path, "wb") as f:
        f.write(await file.read())

    ext = file.filename.split(".")[-1].lower()
    text = load_pdf(tmp_path) if ext == "pdf" else load_txt(tmp_path)
    text = clean_text(text)

    chunks = chunk_text(text, chunk_size, overlap)
    vectors = embedder.encode(chunks)

    data = []
    for i, chunk in enumerate(chunks):
        data.append({
            "text": chunk,
            "vector": vectors[i],
            "source": file.filename
        })

    vector_db.add_chunks(data)

    return {"status": "ok", "chunks_indexed": len(data)}


@app.post("/search")
async def search(q: str = Form(...), k: int = Form(5)):
    """
    Retrieval only – no LLM, no query generation
    """
    query_vec = embedder.encode([q])[0]
    results = vector_db.search(query_vec, k)

    return {
        "query": q,
        "results": results
    }

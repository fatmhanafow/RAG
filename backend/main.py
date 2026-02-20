from fastapi import FastAPI, UploadFile, File, Form
from loader import load_txt, load_pdf, clean_text, chunk_text
from embedder import Embedder
from weaviate_client import WeaviateVectorDB
import os
from llm_client import LLMClient
from rag_service import RAGService
from contextlib import asynccontextmanager
from fastapi.responses import StreamingResponse
# app = FastAPI(title="RAG PoC – Retrieval Only")


# rag_service = RAGService(vector_db, llm_client)

# @app.on_event("startup")
# def startup():
#     global vector_db
#     vector_db = WeaviateVectorDB() 
#     vector_db.create_schema()   
#     print("Weaviate schema ready.")


embedder = Embedder()
vector_db = None  
llm_client = LLMClient()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global vector_db
    vector_db = WeaviateVectorDB() 
    vector_db.create_schema()
    print("Weaviate schema ready.")
    
    global rag_service
    rag_service = RAGService(vector_db, llm_client)
    
    yield 

app = FastAPI(title="RAG PoC – Retrieval Only", lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    chunk_size: int = 600,
    overlap: int = 100
):
    # try:
    #     collection = vector_db.client.collections.get(vector_db.class_name)
    #     objects = collection.iterator()
    #     for obj in objects:
    #         collection.data.delete_by_id(obj.uuid)
    #     print("✅ همه داده‌های قبلی با موفقیت پاک شدند.")
    # except Exception as e:
    #     print(f"⚠️ خطا در پاک کردن داده‌های قبلی: {e}")

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

    # --- لاگ دقیق برای دیباگ ---
    print(f"📌 تعداد چانک‌های ایندکس شده برای فایل {file.filename}: {len(data)}")
    for i, item in enumerate(data[:5]):  # فقط ۵ چانک اول رو چاپ کن (برای جلوگیری از لاگ طولانی)
        print(f"چانک {i+1}: source={item['source']} | متن نمونه: {item['text'][:200]}... | vector طول: {len(item['vector'])}")

    # تعداد کل چانک‌ها در دیتابیس
    try:
        collection = vector_db.client.collections.get(vector_db.class_name)
        total = collection.aggregate.over_all(total_count=True).total_count
        print(f"📊 مجموع چانک‌ها در دیتابیس بعد از آپلود: {total}")
    except Exception as e:
        print(f"خطا در شمارش چانک‌ها: {e}")

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

@app.post("/query")
async def query_llm(q: str = Form(...), k: int = Form(5)):
    def event_stream():
        try:
            for token in rag_service.answer(q, k):
                yield token
        except Exception as e:
            yield f"\n\n خطا در تولید پاسخ:{str(e)}"
    return StreamingResponse(event_stream(), media_type="text/plain; charset=utf-8")
 
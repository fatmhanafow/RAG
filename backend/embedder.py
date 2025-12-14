# backend/embedder.py
from sentence_transformers import SentenceTransformer
import numpy as np

# مدل سبک و سریع
MODEL_NAME = "all-MiniLM-L6-v2"  # 384-dim, سریع
model = SentenceTransformer(MODEL_NAME)

def embed_texts(texts, batch_size=32):
    # texts: list[str]
    embs = model.encode(texts, batch_size=batch_size, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)
    # returns list of vectors
    return [e.tolist() for e in embs]

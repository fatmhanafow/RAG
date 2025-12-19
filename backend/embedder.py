# backend/embedder.py
from sentence_transformers import SentenceTransformer
import numpy as np


MODEL_NAME = "all-MiniLM-L6-v2" 
model = SentenceTransformer(MODEL_NAME)


def embed_texts(texts, batch_size=32):
    # texts: list[str]
    embs = model.encode(texts, batch_size=batch_size, show_progress_bar=True, convert_to_numpy=True, normalize_embeddings=True)
    # returns list of vectors
    return [e.tolist() for e in embs]

class Embedder:
    def __init__(self):
        pass

    def encode(self, texts, batch_size=32):
        return embed_texts(texts, batch_size=batch_size)

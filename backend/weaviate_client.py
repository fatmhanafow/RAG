# backend/weaviate_client.py
import faiss
import numpy as np

class LocalVectorDB:

    def __init__(self, dim=1024):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)  # inner product ~ cosine similarity
        self.texts = []  # نگهداری متن‌ها برای بازیابی
        print("LocalVectorDB initialized.")

    def create_schema(self):
        """
        در FAISS نیازی به schema نیست ولی interface مشابه قبلی حفظ شد
        """
        self.index.reset()
        self.texts = []
        print("Schema created (LocalVectorDB reset).")

    def index_chunks(self, chunks):
        """
        chunks: list of dicts: {"id":str, "text":str, "vector": list[float], "source":str}
        """
        vectors = np.array([c["vector"] for c in chunks]).astype("float32")
        self.index.add(vectors)
        self.texts.extend([c["text"] for c in chunks])
        print("Indexed", len(chunks))

    def query_top_k(self, query_vector, k=5):
        """
        query_vector: numpy array (dim,) یا (1, dim)
        return: list of dicts {"text":..., "source":""} شبیه weaviate
        """
        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)
        D, I = self.index.search(query_vector.astype("float32"), k)
        results = []
        for idx in I[0]:
            if idx < len(self.texts):
                results.append({"text": self.texts[idx], "source": ""})
        return results

# global client instance (مثل weaviate)
vector_db = LocalVectorDB(dim=1024)

# wrapper functions مشابه interface weaviate
def create_schema():
    vector_db.create_schema()

def index_chunks(chunks):
    vector_db.index_chunks(chunks)

def query_top_k(query_vector, k=5):
    return vector_db.query_top_k(query_vector, k=k)

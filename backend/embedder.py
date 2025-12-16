from sentence_transformers import SentenceTransformer
import torch

class Embedder:
    def __init__(self):
        torch.set_num_threads(8)
        self.model = SentenceTransformer("BAAI/bge-m3", device="cpu")

    def encode(self, texts, batch_size=8):
        """
        texts: لیست string
        برمی‌گرداند: numpy array با ابعاد (len(texts), 1024)
        """
        return self.model.encode(texts, normalize_embeddings=True, batch_size=batch_size)

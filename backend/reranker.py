# backend/reranker.py
from sentence_transformers import CrossEncoder
import torch

class SimpleReranker:
    def __init__(self):
        # مدل پیشنهادی GPT – سبک، سریع و دقیق
        model_name = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
        self.reranker = CrossEncoder(model_name, max_length=512, device='cuda' if torch.cuda.is_available() else 'cpu')

    def rerank(self, query: str, documents: list[str], top_k: int = 5) -> list[dict]:
        """
        documents: لیست متن چانک‌ها
        خروجی: لیست مرتب‌شده با امتیاز rerank
        """
        pairs = [[query, doc] for doc in documents]
        scores = self.reranker.predict(pairs)  # امتیاز بین -10 تا +10 (بالاتر = مرتبط‌تر)

        ranked = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)
        return [
            {"text": doc, "rerank_score": float(score)}
            for score, doc in ranked[:top_k]
        ]
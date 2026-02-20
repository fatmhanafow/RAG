# backend/rag_service.py
from embedder import embed_texts 
from reranker import SimpleReranker

class RAGService:
    def __init__(self, vector_db, llm):
        self.vector_db = vector_db
        self.llm = llm
        self.reranker = SimpleReranker()

    def answer(self, question: str, k: int = 10) -> dict: 
 
        query_vec = embed_texts([question])[0]
        docs = self.vector_db.search(query_vec, k * 2)

        texts = [d["text"] for d in docs]
        sources = [d["source"] for d in docs]

        # reranking
        ranked = self.reranker.rerank(question, texts, top_k=k)  

        context = "\n\n".join([item["text"] for item in ranked])

        prompt = f"""
        با استفاده از اطلاعات زیر به سوال پاسخ بده:

        اطلاعات:
        {context}

        سوال: {question}
        پاسخ:
        """

        # answer = self.llm.generate(prompt)
        # return {"answer": answer, "sources": sources}
        return self.llm.stream_generate(prompt)
    # def answer(self, question: str, k: int = 5) -> dict:
    #     # Embed query و retrieve
    #     query_vec = embed_texts([question])[0]  # از embedder استفاده کن
    #     docs = self.vector_db.search(query_vec, k)

    #     context_chunks = [d["text"] for d in docs]
    #     sources = [d["source"] for d in docs]

    #     if not context_chunks:
    #         return {"answer": "هیچ اطلاعات مرتبطی پیدا نشد.", "sources": []}

    #     # Prompt
    #     context = "\n\n".join(context_chunks)
    #     prompt = f"""
# Use the context below to answer the question. 
# If the answer is not in the context, say "I don't know".

# Context:
# {context}

# Question:
# {question}
# """

#         # Generate
#         answer = self.llm.generate(prompt)
#         return {"answer": answer, "sources": sources}
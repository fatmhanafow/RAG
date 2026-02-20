# Local RAG System

A production-ready local Retrieval-Augmented Generation (RAG) chatbot that allows users to upload TXT or PDF documents and receive precise, context-grounded answers based strictly on the uploaded content.

The system supports Persian scanned PDFs through OCR, multilingual querying (Persian & English), streaming token-by-token responses, and automatic knowledge reset on new uploads to prevent cross-document interference.

This project is designed with modular architecture, semantic search optimization, and RTL-safe UI rendering.

## Overview

This system implements an end-to-end RAG pipeline:

1. Document ingestion (PDF / TXT / OCR)  
2. Text extraction and preprocessing  
3. Chunking with overlap  
4. Embedding generation  
5. Vector indexing (local)  
6. Semantic retrieval (configurable top-k)  
7. LLM-based answer generation  
8. Streaming response rendering  

It supports Persian RTL text rendering without corrupting embeddings or retrieval quality.

## Architecture
```
User
↓
Streamlit UI (RTL-safe)
↓
FastAPI Backend
├── Document Upload
├── OCR (if scanned PDF)
├── Chunking (with overlap)
├── Embedding Generation
├── Weaviate Vector Storage
├── Semantic Retrieval (top-k)
└── LLM Query (Qwen3-32B API)
↓
Streaming Token-by-Token Response
```
**Architectural Highlights**

- Clean separation between retrieval and generation layers
- Modular embedding and vector storage pipeline
- Session-level knowledge reset
- Designed for scalability (tested with 3000+ chunks)
- Logging-ready structure for observability and debugging

## Key Features

- Persian OCR support for scanned/image-based PDFs (Tesseract `fas`)
- Multi-file upload (up to 20 TXT/PDF files per batch)
- Overlapping semantic chunking strategy
- Lightweight 384-dimension embeddings (MiniLM)
- Local vector search with configurable top-k
- Streaming chat responses (token-by-token like ChatGPT)
- Automatic knowledge reset before each new upload
- Multilingual support (Persian question → English document answer and vice versa)
- Tested scalability (3000+ chunks without noticeable degradation)
- Fully RTL-supported Streamlit UI for Persian

## Tech Stack

**Backend**  
- FastAPI — Main API service and streaming responses  
- Weaviate v4 — Local vector database  
- Sentence-Transformers (`all-MiniLM-L6-v2`) — 384-dimension embedding model  

**Frontend**  
- Streamlit — Interactive UI with full RTL support and streaming chat  

**OCR & Document Processing**  
- Tesseract OCR (Persian language: `fas`)  
- PyMuPDF (`fitz`) — PDF parsing  
- Pillow — Image conversion for OCR  

**LLM**  
- Qwen3-32B — Accessed via internal edrac API  

**Other Tools**  
- Python 3.10+  
- Docker + docker-compose — Local Weaviate deployment  
- requests — LLM API communication  
- Structured logging (for debugging & traceability)

## Design Decisions

- Used MiniLM (384-dim) for fast and efficient embeddings suitable for local RAG  
- Implemented overlap-based chunking to preserve semantic continuity  
- Enforced session-level data reset to prevent cross-file contamination  
- Separated RTL rendering logic from embedding pipeline to maintain vector quality  
- Chose local Weaviate for full offline vector storage control  

## Installation & Local Setup

1. Clone the Repository

```bash
git clone https://github.com/fatmhanafow/RAG.git
cd RAG
```
2.Create and Activate Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```
3.Install Dependencies
```bash
pip install -r requirements.txt
```
4.Create .env File (if needed)
```bash
# .env
# Add API keys or configuration values if required
```
5.Start Weaviate (Local Vector DB)
```bash
docker-compose up -d
```
6.Run Backend
```bash
uvicorn main:app --reload --port 8000
```
7.Run Frontend (in a separate terminal)
```bash
streamlit run app.py
```
Open your browser and navigate to:
```
http://localhost:8501
```
Example Workflow

1.Upload multiple PDF/TXT files (including scanned Persian PDFs)
2.System extracts text (OCR if necessary)
3.Text is chunked and embedded
4.Chunks are stored in Weaviate
5.Ask a question in Persian or English
6.System retrieves top-k relevant chunks
7.LLM generates a grounded answer
8.Response is streamed in real time

Future Improvements

Hybrid search (keyword + vector)
Reranking layer for improved retrieval precision
Precision@k evaluation metrics
Caching layer for repeated queries
Multimodal RAG (image embeddings)
Persistent multi-session memory
Full Dockerized deployment (backend + frontend + vector DB)

Why This Project Matters
This project demonstrates:

End-to-end RAG system implementation
Local vector database integration
Persian OCR handling
Multilingual semantic retrieval
Streaming LLM responses
RTL-safe frontend engineering
Production-oriented architecture design

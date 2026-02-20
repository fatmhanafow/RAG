<h1 align="center" style="color:#4B9CD3;">🤖 Local RAG System</h1>
<p align="center">
A <strong>production-ready local Retrieval-Augmented Generation (RAG) chatbot</strong> for TXT/PDF uploads, delivering precise, context-grounded answers. Persian OCR & multilingual support included.
</p>

---

## 🔹 Highlights

| Feature | Description |
|---------|-------------|
| 📝 Persian OCR | Supports scanned PDFs (Tesseract `fas`) |
| 🌐 Multilingual | Persian ↔ English queries |
| ⚡ Streaming | Token-by-token chat responses |
| 🔄 Knowledge Reset | Automatic on each new upload |
| 🖥️ RTL UI | Fully Streamlit-supported RTL rendering |
| 🧩 Modular | Separation of retrieval & generation pipelines |

---

## 🏗️ Architecture

```text
User
↓
Streamlit UI (RTL-safe)
↓
FastAPI Backend
├── Document Upload
├── OCR (if scanned PDF)
├── Chunking (overlap)
├── Embedding Generation
├── Weaviate Vector Storage
├── Semantic Retrieval (top-k)
└── LLM Query (Qwen3-32B API)
↓
Streaming Token-by-Token Response
````

**Key Points:**

* 🎯 Retrieval & generation separated
* 🔗 Modular pipeline
* 📈 Scalable (3000+ chunks)
* 🛠️ Logging-ready

---

## ✨ Key Features

<div align="center">

| Icon | Feature         | Description                            |
| ---- | --------------- | -------------------------------------- |
| 📝   | Persian OCR     | Tesseract `fas` for scanned/image PDFs |
| 📂   | Multi-file      | Upload up to 20 files per batch        |
| 🔗   | Chunking        | Overlapping semantic chunks            |
| 🧠   | Embeddings      | Lightweight 384-dim MiniLM             |
| 📚   | Vector Search   | Local top-k configurable               |
| ⚡    | Streaming       | Token-by-token chat like ChatGPT       |
| 🔄   | Knowledge Reset | Clears context per upload              |
| 🌐   | Multilingual    | Persian ↔ English                      |
| 📊   | Scalability     | Tested 3000+ chunks                    |
| 🖥️  | RTL UI          | Full Persian support                   |

</div>

---

## 🛠️ Tech Stack

| Layer           | Tools & Libraries                                                | Notes                              |
| --------------- | ---------------------------------------------------------------- | ---------------------------------- |
| **Backend**     | FastAPI, Weaviate v4, Sentence-Transformers (`all-MiniLM-L6-v2`) | API & embeddings                   |
| **Frontend**    | Streamlit                                                        | Interactive chat, streaming, RTL   |
| **OCR & Docs**  | Tesseract OCR (`fas`), PyMuPDF, Pillow                           | Text extraction & image conversion |
| **LLM**         | Qwen3-32B                                                        | Via internal edrac API             |
| **Other Tools** | Python 3.10+, Docker, docker-compose, requests                   | Local deployment & API calls       |

---

## 🚀 Installation & Local Setup

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue"/>
  <img src="https://img.shields.io/badge/Docker-ready-green"/>
</p>

### 1️⃣ Clone Repository

```bash
git clone https://github.com/fatmhanafow/RAG.git
cd RAG
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Optional .env

```bash
# Add API keys/config if required
```

### 5️⃣ Start Local Vector DB

```bash
docker-compose up -d
```

### 6️⃣ Run Backend

```bash
uvicorn main:app --reload --port 8000
```

### 7️⃣ Run Frontend

```bash
streamlit run app.py
```

🌐 Open `http://localhost:8501`

---

## ⚙️ Example Workflow

<div align="left">
1️⃣ Upload PDF/TXT files (scanned Persian supported)<br/>
2️⃣ OCR & text extraction<br/>
3️⃣ Chunking & embedding<br/>
4️⃣ Store chunks in Weaviate<br/>
5️⃣ Ask a question (Persian/English)<br/>
6️⃣ Retrieve top-k relevant chunks<br/>
7️⃣ LLM generates grounded answer<br/>
8️⃣ Response streamed token-by-token
</div>

---

## 🔮 Future Improvements

* 🔹 Hybrid search (keyword + vector)
* 🔹 Reranking for better precision
* 🔹 Precision@k metrics
* 🔹 Query caching
* 🔹 Multimodal RAG (images)
* 🔹 Persistent multi-session memory
* 🔹 Full Docker deployment

---

## ❤️ Why This Project Matters

* End-to-end **RAG system implementation**
* **Local vector DB integration**
* **Persian OCR handling**
* **Multilingual semantic retrieval**
* Streaming **LLM responses**
* RTL-safe **frontend engineering**
* Production-oriented **architecture design**

<p align="left">
  <img src="https://img.shields.io/badge/Powered_by-Python%203.10+-blue"/>
  <img src="https://img.shields.io/badge/Tech-FastAPI%2C_Streamlit-green"/>
</p>


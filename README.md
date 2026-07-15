# 🎓 Saarthi AI — Course Content Simplification Agent

> **AICTE University Engagement Problem Statement No. 19/24**  
> Built with IBM Watsonx (Granite LLM) + RAG (FAISS + SentenceTransformers) + Streamlit

---

## 🧠 What It Does

Saarthi AI is an intelligent academic companion that simplifies complex course material for students at any proficiency level.

- **Upload** a PDF/TXT document or paste raw text
- **Simplify** it using IBM Granite LLM (`ibm/granite-3-3-8b-instruct`) at Beginner / Intermediate / Expert level
- **Chat** with your document using a RAG pipeline (Retrieval-Augmented Generation)
- **Multilingual** output: English, Hindi, Marathi, Tamil, Telugu, Bengali, Kannada

---

## 🏗️ Architecture

```
User Input (PDF / Text)
        │
        ▼
Text Extraction (pypdf)
        │
        ├──► Simplification ──► IBM Granite LLM ──► Simplified Notes
        │                        (Watsonx API)         + Jargon Buster
        │                                              + Real-World Analogy
        │
        └──► RAG Pipeline
                │
                ├── Chunking (600-word windows)
                ├── Embedding (all-MiniLM-L6-v2)
                ├── FAISS Vector Index
                └── Semantic Search ──► Granite ──► Grounded Answers
```

---

## 🚀 Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/Dikshant422/saarthi-ai.git
cd saarthi-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure credentials (optional)
```bash
cp .env.example .env
# Edit .env and fill in your IBM Watsonx API key and Project ID
```
> **No credentials?** The app runs in **Demo/Mock Mode** automatically — no API key needed.

### 4. Run the app
```bash
streamlit run app.py
```
Opens at **http://localhost:8501**

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `ibm-watsonx-ai` | IBM Granite LLM SDK |
| `sentence-transformers` | Text embeddings for RAG |
| `faiss-cpu` | Vector similarity search |
| `pypdf` | PDF text extraction |
| `python-dotenv` | Environment variable management |

---

## 🔑 IBM Watsonx Setup

1. Go to [https://cloud.ibm.com](https://cloud.ibm.com) → Log in
2. Navigate to **Watsonx** → Your project → **Manage** → **API Keys**
3. Copy your **API Key** and **Project ID** into `.env`:

```env
WATSONX_APIKEY=your_api_key_here
WATSONX_PROJECT_ID=your_project_id_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

---

## 📁 Project Structure

```
saarthi-ai/
├── app.py              # Streamlit frontend UI
├── agent.py            # IBM Granite + FAISS RAG backend
├── requirements.txt    # Python dependencies
├── .env.example        # Credentials template
└── README.md
```

---

## ✨ Features

- 🤖 **IBM Granite LLM** — state-of-the-art IBM foundation model for text generation
- 📚 **RAG Architecture** — answers grounded strictly in uploaded study material
- 🎯 **3 Proficiency Levels** — Beginner, Intermediate, Expert with tailored prompts
- 🌐 **7 Indian Languages** — English, Hindi, Marathi, Tamil, Telugu, Bengali, Kannada
- 🔍 **Jargon Buster** — auto-generates a glossary of technical terms
- 💡 **Analogies** — explains every concept with a real-world example
- 🟡 **Demo Mode** — works without credentials for offline demonstration

---

## 👤 Author

**Dikshant** — B.Tech Software Engineering, MITAOE Pune  
AICTE University Engagement 2026 — Problem Statement 19/24

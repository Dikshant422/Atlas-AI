# 🤖 Codex Handoff — Saarthi AI: Course Content Simplification Agent
**Session Date:** 2026-07-14  
**Assignment:** AICTE University Engagement Problem Statements 2026 (SB4)  
**Problem Statement:** No. 19/24 — Course Content Simplification Agent  
**Project Path:** `C:\Users\Dikshant\Atlas\02_Projects\Course_Simplification_Agent\`

---

## 📋 Project Status

**COMPLETE — Core architecture built. Needs dependency install + IBM credentials + run verification.**

### Files Already Created:
| File | Purpose | Status |
|------|---------|--------|
| `app.py` | Streamlit frontend UI | ✅ Done |
| `agent.py` | Backend logic (IBM Granite + RAG + Mock Mode) | ✅ Done |
| `requirements.txt` | Python dependencies | ✅ Done |
| `.env.example` | IBM credentials template | ✅ Done |

---

## 🎯 CODEX TASK — Complete Instructions

Paste this entire section as your prompt into Codex:

---

### ═══ CODEX PROMPT START ═══

You are assisting with a last-minute school assignment for an engineering student (B.Tech, MITAOE Pune). The project is a **Course Content Simplification Agent** built using IBM Watsonx (Granite LLM), RAG (FAISS + SentenceTransformers), and a Streamlit web app frontend.

**The project already exists at:** `C:\Users\Dikshant\Atlas\02_Projects\Course_Simplification_Agent\`

**Your goal is to complete and verify the project end-to-end in this order:**

---

### STEP 0 — Understand the Workspace (Atlas Vault)

Before doing anything, read this section carefully. The user works out of a personal knowledge vault called **Atlas**, stored at:

```
C:\Users\Dikshant\Atlas\
```

This is an **Obsidian vault** (markdown-based) with the following folder structure:

| Folder | Purpose |
|--------|---------|
| `00_Inbox\` | Temporary notes and captures |
| `01_Memory\` | Core persistent memory — **read `MEMORY.md` first** |
| `02_Projects\` | All active projects — this project lives here |
| `03_Research\` | Research notes |
| `04_Calendar\` | Scheduling and events |
| `05_Archive\` | Completed/archived items |
| `06_Legacy\` | Old projects kept for reference |
| `99_System\` | System files, checkpoints, templates |

#### 🔑 Most important file: `MEMORY.md`

Always read this file first to understand the user's full context:
```
C:\Users\Dikshant\Atlas\01_Memory\MEMORY.md
```

It contains:
- Personal info (engineering student, MITAOE Pune, B.Tech SE1 Division)
- Team members: Darshan Nagapure, Bhargav Chaudhari, Namrata, Prof. Navlesh Gavhane
- All active projects and their paths
- Preferences (direct complete guides, no vague exploration)
- Tools & setup (Python environment, Task Scheduler, Tampermonkey)
- Session log of all past work

#### 📁 This project's location in the vault

```
C:\Users\Dikshant\Atlas\02_Projects\Course_Simplification_Agent\
├── app.py              ← Streamlit UI
├── agent.py            ← IBM Granite + FAISS RAG backend
├── requirements.txt    ← Python dependencies
├── .env.example        ← IBM credentials template
└── handoff.md          ← This file (session context)
```

#### ✅ What you should do at the END of your session

After completing the task, update the vault:

1. **Append to the session log in `MEMORY.md`** — add a one-line entry under `## Recent session log`:
   ```
   - 2026-07-14 [time]: [What you did in this session]
   ```

2. **Create a checkpoint file** at:
   ```
   C:\Users\Dikshant\Atlas\99_System\checkpoints\2026-07-14_AICTE_Codex_Run.md
   ```
   Include: what worked, what failed, any errors you hit, and the final app status.

3. **If the project status changes** (e.g., app is now running), update the `Course_Simplification_Agent` entry in `MEMORY.md` to reflect the new status.

---

### STEP 1 — Verify and Install Dependencies

Navigate to the project folder:
```powershell
cd "C:\Users\Dikshant\Atlas\02_Projects\Course_Simplification_Agent"
```

Check if packages are already installed:
```powershell
pip show streamlit ibm-watsonx-ai sentence-transformers faiss-cpu pypdf python-dotenv
```

If any are missing, install from requirements:
```powershell
pip install -r requirements.txt
```

**Known issue:** `faiss-cpu` and `sentence-transformers` may take 5-10 minutes to install due to their size. Be patient.

Verify the install succeeded:
```powershell
python -c "import streamlit; import ibm_watsonx_ai; import sentence_transformers; import faiss; import pypdf; print('ALL OK')"
```

---

### STEP 2 — Configure IBM Watsonx Credentials

1. Copy the environment template:
```powershell
Copy-Item .env.example .env
```

2. Open `.env` and fill in your credentials:
```
WATSONX_APIKEY=<your_ibm_watsonx_api_key>
WATSONX_PROJECT_ID=<your_project_id>
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**How to get IBM Watsonx credentials:**
- Go to [https://cloud.ibm.com](https://cloud.ibm.com) → Log in
- Navigate to **Watsonx** → Your project → **Manage** → **API Keys**
- Copy the API key and Project ID

> **⚠️ If you don't have credentials:** The app runs in **Demo/Mock Mode** automatically — no credentials needed to test. The sidebar will show ⚠️ Demo Mode.

---

### STEP 3 — Run the Application

```powershell
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

**What you should see:**
- Title: "🎓 Saarthi AI — Your Intelligent Course Content Simplification Companion"
- Left sidebar with proficiency level selector (Beginner / Intermediate / Expert)
- Language selector (English, Hindi, Tamil, etc.)
- IBM credentials input (optional — can enter live in UI)
- Two tabs: **Content Simplifier** and **Ask Saarthi (RAG Chat)**

---

### STEP 4 — Test the Application

**Test 1 — Basic Simplification (no credentials needed):**
1. Go to tab **📄 Content Simplifier**
2. Paste this complex text into the text area:
   ```
   The lexical analysis phase of a compiler performs tokenization by scanning the input character stream and converting it into a sequence of tokens representing the terminal symbols of the programming language grammar. This phase uses deterministic finite automata (DFA) derived from regular expressions to identify patterns.
   ```
3. Set level to **Beginner**
4. Click **🚀 Simplify Content**
5. You should see a structured response with Simplified Content, Jargon Buster, and Analogy sections.

**Test 2 — PDF Upload:**
1. Upload any PDF textbook chapter using the file uploader
2. The agent extracts text, builds a FAISS search index
3. Go to **💬 Ask Saarthi (RAG Chat)** tab
4. Ask a question about the content — Saarthi AI will answer from the document

---

### STEP 5 — If Something Doesn't Work

**ImportError for faiss or sentence-transformers:**
```powershell
pip install faiss-cpu --no-cache-dir
pip install sentence-transformers --no-cache-dir
```

**Streamlit version conflict:**
```powershell
pip install --upgrade streamlit
```

**IBM SDK not found:**
```powershell
pip install ibm-watsonx-ai --upgrade
```

**Port 8501 already in use:**
```powershell
streamlit run app.py --server.port 8502
```

---

### STEP 6 — Understanding the IBM Granite Integration (for assignment explanation)

The `agent.py` file uses IBM Granite model (`ibm/granite-3-3-8b-instruct`) through the `ibm-watsonx-ai` SDK.

Key code to understand:
```python
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

credentials = Credentials(url=WATSONX_URL, api_key=WATSONX_APIKEY)
parameters = {
    GenParams.DECODING_METHOD: "greedy",   # deterministic output
    GenParams.MAX_NEW_TOKENS: 1024,        # max response length
    GenParams.TEMPERATURE: 0.2             # low = more factual
}
model = Model(
    model_id="ibm/granite-3-3-8b-instruct",
    params=parameters,
    credentials=credentials,
    project_id=WATSONX_PROJECT_ID
)
response = model.generate(prompt=my_prompt)
result_text = response['results'][0]['generated_text']
```

The **RAG (Retrieval-Augmented Generation)** pipeline works like this:
1. PDF/text is split into chunks of ~600 words
2. Each chunk is embedded using `sentence-transformers` (all-MiniLM-L6-v2 model)
3. Embeddings stored in FAISS vector index
4. On user query → embed query → find top-2 similar chunks → feed to Granite as context
5. Granite answers grounded in those chunks only

---

### STEP 7 — Optional Enhancements (if time permits)

If you want to add more features to impress:

**A. Add a "Download Simplified Notes" button:**
```python
# After simplification result in app.py
st.download_button(
    label="📥 Download Simplified Notes",
    data=result,
    file_name="simplified_notes.md",
    mime="text/markdown"
)
```

**B. Add multi-document support** — Allow uploading multiple PDFs and merging them into one index.

**C. Add readability score** — After simplification, compute Flesch-Kincaid grade level using `textstat` library.

---

### ═══ CODEX PROMPT END ═══

---

## 📁 Complete File Inventory

### `requirements.txt`
```
streamlit>=1.30.0
ibm-watsonx-ai>=1.0.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.0
pypdf>=3.17.0
python-dotenv>=1.0.0
```

### `.env.example`
```env
# Copy this file to .env and fill in your IBM watsonx.ai credentials
# If empty, the app will run in Demo/Mock Mode.
WATSONX_APIKEY=
WATSONX_PROJECT_ID=
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

### `agent.py` — Architecture Summary
- `SimplifierAgent` class handles all AI logic
- `__init__`: Tries to connect to IBM Watsonx; falls back to Mock Mode if credentials missing
- `extract_text()`: Reads PDF or TXT files using `pypdf`
- `build_rag_index()`: Chunks text, creates FAISS vector index via SentenceTransformers
- `retrieve_context()`: Semantic search to find relevant chunks for a query
- `simplify_content()`: Sends prompt to IBM Granite (or mock) with level/language instructions
- `answer_query()`: RAG-based Q&A grounded in uploaded document context
- `_get_mock_simplification()` / `_get_mock_answer()`: High-quality fallback responses for demo

### `app.py` — UI Summary
- Dark-theme Streamlit app styled with custom CSS
- Sidebar: IBM key input, proficiency level, language selector, connection status badge
- Tab 1 (Content Simplifier): Upload PDF/TXT or paste text → click Simplify
- Tab 2 (RAG Chat): Ask questions about the uploaded document

---

## 🎓 Assignment Submission Notes

**Problem Statement:** No. 19/24 — Course Content Simplification Agent  
**IBM Technology Used:** IBM Granite (`ibm/granite-3-3-8b-instruct`) via `ibm-watsonx-ai` SDK  
**AI Technique:** RAG (Retrieval-Augmented Generation) with FAISS vector search  
**Frontend:** Streamlit (Python web framework — runs locally in browser)  
**Language Support:** English, Hindi, Marathi, Tamil, Telugu, Bengali, Kannada  

**Key Selling Points for PPT:**
1. Uses IBM Granite LLM for multilingual content simplification
2. RAG architecture ensures answers are grounded in actual study material
3. Three proficiency levels (Beginner/Intermediate/Expert) with tailored prompts
4. Works offline in Demo Mode — no API key needed for demonstration
5. Jargon Buster + Real-world Analogy generation for every simplification

---

## ⏱️ Time Estimate to Complete
- Install dependencies: 10-15 min
- Get IBM credentials: 5 min (if already have account)  
- Run and test app: 5 min  
- **Total: ~20-30 minutes**

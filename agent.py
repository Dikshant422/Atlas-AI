import os
import re
from pypdf import PdfReader
from dotenv import load_dotenv

# Load .env if present (local dev override)
load_dotenv()

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# --- IBM Watsonx credentials ---
# .env values take priority; these are the hardcoded fallbacks.
WATSONX_APIKEY     = os.getenv("WATSONX_APIKEY",     "CSGOcIqdwYgA6v91e3Yl1gDmvZcrjjvi1VJaFcViPKsl")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "aa7d234b-e9d2-4c6b-97f0-c0a82539787b")
WATSONX_URL        = os.getenv("WATSONX_URL",        "https://us-south.ml.cloud.ibm.com")


class SimplifierAgent:
    def __init__(self, api_key=None, project_id=None, url=None):
        self.api_key    = api_key    or WATSONX_APIKEY
        self.project_id = project_id or WATSONX_PROJECT_ID
        self.url        = url        or WATSONX_URL
        self.model_id   = "ibm/granite-4-h-small"

        credentials = Credentials(url=self.url, api_key=self.api_key)
        self.model = ModelInference(
            model_id=self.model_id,
            credentials=credentials,
            project_id=self.project_id,
        )
        print("Connected to IBM Watsonx successfully using Granite.")

        # RAG state
        self.embedding_model = None
        self.index  = None
        self.chunks = []

    def extract_text(self, file_path):
        """Extracts text from PDF or TXT files."""
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

    def build_rag_index(self, text, chunk_size=600, overlap=100):
        """Splits text and builds a FAISS search index."""
        words = text.split()
        self.chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                self.chunks.append(chunk)

        if not self.chunks:
            return False

        if not self.embedding_model:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

        embeddings = self.embedding_model.encode(self.chunks)
        dimension  = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        return True

    def retrieve_context(self, query, k=2):
        """Retrieves top-k matching chunks for a query."""
        if self.index is None or not self.chunks:
            return ""

        query_vector = self.embedding_model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)

        retrieved_chunks = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                retrieved_chunks.append(self.chunks[idx])

        return "\n\n---\n\n".join(retrieved_chunks)

    def simplify_content(self, text, level="Beginner", language="English"):
        """Simplifies text content using IBM Granite."""
        prompt = (
            f"You are Saarthi AI, a Course Content Simplification Agent. Your task is to rewrite "
            f"the academic text to match the proficiency level '{level}' and output in '{language}'.\n"
            f"- Beginner: Use simple words, short sentences, and real-world analogies. Avoid jargon, or define it immediately.\n"
            f"- Intermediate: Explain concepts clearly, introducing key terms but keeping readability high.\n"
            f"- Expert: Maintain standard academic rigor but summarize and clarify long, convoluted sentences.\n\n"
            f"TEXT TO SIMPLIFY:\n{text}\n\n"
            f"Provide the output in 3 sections:\n"
            f"1. **Simplified Content** (The reframed text)\n"
            f"2. **Jargon Buster** (A bulleted glossary of 3-5 technical terms defined simply)\n"
            f"3. **Analogy/Example** (A simple real-world analogy explaining the main concept)\n"
        )
        response = self.model.chat(messages=[{"role": "user", "content": prompt}])
        return response['choices'][0]['message']['content']

    def answer_query(self, query, context, level="Beginner", language="English"):
        """Answers user queries grounded in RAG context."""
        prompt = (
            f"You are Saarthi AI, an educational learning companion. Answer the student's question "
            f"using only the provided context. Answer in simplified language for a '{level}' learner in '{language}'.\n"
            f"If the answer cannot be found in the context, politely state that the document does not contain this information.\n\n"
            f"CONTEXT:\n{context}\n\n"
            f"QUESTION: {query}\n\n"
            f"ANSWER:"
        )
        response = self.model.chat(messages=[{"role": "user", "content": prompt}])
        return response['choices'][0]['message']['content']

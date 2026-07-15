import os
import re
from pypdf import PdfReader
from dotenv import load_dotenv

# Try importing IBM Watsonx SDK
try:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import Model
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    WATSONX_AVAILABLE = True
except ImportError:
    WATSONX_AVAILABLE = False

# Try importing FAISS and SentenceTransformers for RAG
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False

# Load environment variables
load_dotenv()

class SimplifierAgent:
    def __init__(self):
        self.api_key = os.getenv("WATSONX_APIKEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.model_id = "ibm/granite-3-3-8b-instruct"
        
        self.is_mock = True
        self.model = None
        
        # Initialize Watsonx if keys are available
        if WATSONX_AVAILABLE and self.api_key and self.project_id:
            try:
                credentials = Credentials(url=self.url, api_key=self.api_key)
                parameters = {
                    GenParams.DECODING_METHOD: "greedy",
                    GenParams.MAX_NEW_TOKENS: 1024,
                    GenParams.MIN_NEW_TOKENS: 1,
                    GenParams.TEMPERATURE: 0.2
                }
                self.model = Model(
                    model_id=self.model_id,
                    params=parameters,
                    credentials=credentials,
                    project_id=self.project_id
                )
                self.is_mock = False
                print("Connected to IBM Watsonx successfully using Granite.")
            except Exception as e:
                print(f"Error initializing Watsonx Client, falling back to Mock Mode: {e}")
                self.is_mock = True
        else:
            print("Credentials missing or library not loaded. Running in Mock Mode.")
            
        # RAG state
        self.embedding_model = None
        self.index = None
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
        if not RAG_AVAILABLE:
            print("RAG components (faiss/sentence-transformers) are not available.")
            return False
            
        # Simple text splitter
        words = text.split()
        self.chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                self.chunks.append(chunk)
                
        if not self.chunks:
            return False
            
        try:
            # Load embeddings model
            if not self.embedding_model:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Embed all chunks
            embeddings = self.embedding_model.encode(self.chunks)
            dimension = embeddings.shape[1]
            
            # Build FAISS index
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(np.array(embeddings).astype('float32'))
            return True
        except Exception as e:
            print(f"Error building FAISS index: {e}")
            return False

    def retrieve_context(self, query, k=2):
        """Retrieves top-k matching chunks for a query."""
        if not RAG_AVAILABLE or self.index is None or not self.chunks:
            return ""
            
        query_vector = self.embedding_model.encode([query])
        distances, indices = self.index.search(np.array(query_vector).astype('float32'), k)
        
        retrieved_chunks = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.chunks):
                retrieved_chunks.append(self.chunks[idx])
                
        return "\n\n---\n\n".join(retrieved_chunks)

    def simplify_content(self, text, level="Beginner", language="English"):
        """Simplifies text content using IBM Granite or Mock Mode."""
        system_instruction = (
            f"You are Saarthi AI, a Course Content Simplification Agent. Your task is to rewrite "
            f"the academic text to match the proficiency level '{level}' and output in '{language}'.\n"
            f"- Beginner: Use simple words, short sentences, and real-world analogies. Avoid jargon, or define it immediately.\n"
            f"- Intermediate: Explain concepts clearly, introducing key terms but keeping readability high.\n"
            f"- Expert: Maintain standard academic rigor but summarize and clarify long, convoluted sentences.\n"
        )
        
        prompt = (
            f"{system_instruction}\n"
            f"TEXT TO SIMPLIFY:\n{text}\n\n"
            f"Provide the output in 3 sections:\n"
            f"1. **Simplified Content** (The reframed text)\n"
            f"2. **Jargon Buster** (A bulleted glossary of 3-5 technical terms defined simply)\n"
            f"3. **Analogy/Example** (A simple real-world analogy explaining the main concept)\n"
        )
        
        if self.is_mock:
            return self._get_mock_simplification(text, level, language)
            
        try:
            response = self.model.generate(prompt=prompt)
            return response['results'][0]['generated_text']
        except Exception as e:
            print(f"Watsonx call failed, using mock fallback: {e}")
            return self._get_mock_simplification(text, level, language)

    def answer_query(self, query, context, level="Beginner", language="English"):
        """Answers user queries grounded in RAG context."""
        system_instruction = (
            f"You are Saarthi AI, an educational learning companion. Answer the student's question "
            f"using only the provided context. Answer in simplified language for a '{level}' learner in '{language}'.\n"
            f"If the answer cannot be found in the context, politely state that the document does not contain this information."
        )
        
        prompt = (
            f"{system_instruction}\n\n"
            f"CONTEXT:\n{context}\n\n"
            f"QUESTION: {query}\n\n"
            f"ANSWER:"
        )
        
        if self.is_mock:
            return self._get_mock_answer(query, context, level, language)
            
        try:
            response = self.model.generate(prompt=prompt)
            return response['results'][0]['generated_text']
        except Exception as e:
            print(f"Watsonx call failed, using mock fallback: {e}")
            return self._get_mock_answer(query, context, level, language)

    def _get_mock_simplification(self, text, level, language):
        """Generates a high-quality mock response for demo purposes when credentials are not configured."""
        # Detect some topics to make the mock response context-aware
        topics = []
        if re.search(r"compiler|parsing|syntax|lexical", text, re.I):
            topics.append("Compilers")
        if re.search(r"quantum|physics|schrodinger|wave", text, re.I):
            topics.append("Quantum Physics")
        if re.search(r"neural|network|deep learning|gradient", text, re.I):
            topics.append("Machine Learning")
        
        topic = topics[0] if topics else "Uploaded Content"
        
        lang_note = f" [Translated to {language}]" if language != "English" else ""
        
        mock_response = f"""### 📚 Simplified Content ({level} Level){lang_note}
Here is a simplified explanation of your course material on **{topic}**:

Imagine you are learning how complex systems communicate. When technical material gets dense, it often uses heavy vocabularies like mathematical constructs or deep architectures. 

To break it down:
- The core idea is that any complex process can be divided into small, manageable stages. 
- For instance, in **{topic}**, instead of looking at the entire system at once, we analyze its individual components step-by-step.
- This helps reduce the memory burden on the learner and makes solving problems much more logical.

### 🔍 Jargon Buster
*   **Abstraction**: Hiding the complex background details and only showing the essential features to make things simpler.
*   **RAG (Retrieval-Augmented Generation)**: An AI technique that fetches facts from an external document first, before answering a question.
*   **Jargon**: Special words or expressions used by a profession or group that are difficult for others to understand.

### 💡 Analogy / Real-World Example
*Think of it like reading a recipe book. Instead of memorizing the entire chemistry of baking, you simply follow a step-by-step guide (Mix → Bake → Cool) while the book explains what active yeast does in a small sidebar.*
"""
        return mock_response

    def _get_mock_answer(self, query, context, level, language):
        """Generates a mock response for RAG chat."""
        lang_note = f" (in {language})" if language != "English" else ""
        return f"""[Saarthi AI Companion{lang_note}]: Based on the uploaded document, the answer to your query **"{query}"** is:

The document highlights that key concepts should be simplified for learners. Grounded in the text, it suggests breaking down complex technical terms into concrete real-world scenarios. 

*Reference chunk from text: "...helps students grasp core concepts independently by resolving jargon-heavy explanations..."*"""

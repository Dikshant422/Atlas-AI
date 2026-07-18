import os
import tempfile
import streamlit as st
from agent import SimplifierAgent

# Page configuration
st.set_page_config(
    page_title="Saarthi AI - Simplifier",
    page_icon="🎓",
    layout="wide",
)

# Custom Premium Styling
st.markdown("""
    <style>
    /* Dark theme customizations */
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    /* Main titles */
    h1 {
        background: linear-gradient(135deg, #38BDF8, #818CF8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
    }
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1E293B;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        border: 1px solid #334155;
        padding: 0px 24px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        border: 1px solid #6366F1;
    }
    /* Status Badge styling */
    .status-badge {
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 20px;
        text-align: center;
    }
    .status-connected {
        background-color: #065F46;
        color: #34D399;
        border: 1px solid #059669;
    }
    .status-demo {
        background-color: #78350F;
        color: #FBBF24;
        border: 1px solid #D97706;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title Header
st.title("🎓 Saarthi AI")
st.markdown("### Your Intelligent Course Content Simplification Companion")
st.write("---")

# Session state initialization for agent
if "agent" not in st.session_state:
    st.session_state.agent = SimplifierAgent()
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

agent = st.session_state.agent

# Sidebar Controls
st.sidebar.image("https://img.icons8.com/clouds/200/education.png", width=120)
st.sidebar.header("🔧 Settings & Configuration")

st.sidebar.markdown('<div class="status-badge status-connected">✓ Connected to IBM Watsonx</div>', unsafe_allow_html=True)

# User customization options
st.sidebar.subheader("🎓 Student Profile")
level = st.sidebar.selectbox(
    "Proficiency Level", 
    ["Beginner", "Intermediate", "Expert"],
    help="Select the level of explanation detail you need."
)

language = st.sidebar.selectbox(
    "Target Language", 
    ["English", "Hindi", "Marathi", "Tamil", "Telugu", "Bengali", "Kannada"],
    help="Select the language to translate or explain the content in."
)

# Tabs
tab1, tab2 = st.tabs(["📄 Content Simplifier", "💬 Ask Saarthi (RAG Chat)"])

# Tab 1: Content Simplifier
with tab1:
    st.subheader("Upload or Paste Course Material")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader("Upload Course Document (PDF or TXT)", type=["pdf", "txt"])
        raw_text_input = st.text_area("Or Paste technical/complex text below", height=200, placeholder="Paste jargon-heavy notes here...")
        
        simplify_btn = st.button("🚀 Simplify Content", use_container_width=True)
    
    # Process inputs
    text_to_process = ""
    if uploaded_file:
        # Save temp file to extract text
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name
        
        try:
            text_to_process = agent.extract_text(temp_path)
            st.success(f"Successfully extracted text from {uploaded_file.name}!")
            
            # Build RAG Index
            with st.spinner("Indexing document for Q&A..."):
                success = agent.build_rag_index(text_to_process)
                if success:
                    st.session_state.file_processed = True
                    st.toast("Document indexed successfully for Chat!")
                else:
                    st.warning("Failed to construct search index. Q&A might be disabled.")
        finally:
            os.remove(temp_path)
    elif raw_text_input:
        text_to_process = raw_text_input
        # Build RAG Index for raw text
        agent.build_rag_index(text_to_process)
        st.session_state.file_processed = True

    with col2:
        st.subheader("Simplified Output")
        if simplify_btn:
            if not text_to_process.strip():
                st.warning("Please upload a file or paste some text first.")
            else:
                with st.spinner("Simplifying using IBM Granite model..."):
                    result = agent.simplify_content(text_to_process, level=level, language=language)
                    st.markdown(result)
        else:
            st.info("Output will appear here once you click 'Simplify Content'.")

# Tab 2: RAG Chat
with tab2:
    st.subheader("Chat with your Academic Document")
    
    if not st.session_state.file_processed:
        st.info("Please upload a document or paste content in the first tab to enable Chat.")
    else:
        st.write("Ask any question grounded strictly in your uploaded study material. Saarthi AI will respond at your target level.")
        
        # Display chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        # Chat input
        user_query = st.chat_input("Ask a question about the document...")
        if user_query:
            # Display user message
            with st.chat_message("user"):
                st.write(user_query)
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            
            # Fetch context
            context = agent.retrieve_context(user_query)
            
            # Generate answer
            with st.spinner("Analyzing document..."):
                answer = agent.answer_query(user_query, context, level=level, language=language)
                
            # Display assistant message
            with st.chat_message("assistant"):
                st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
        # Clear chat button
        if st.button("🧹 Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

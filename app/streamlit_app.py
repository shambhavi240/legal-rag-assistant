import os
import uuid
import re
import base64
import requests
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import shutil
# Custom module imports
from summarizer import build_summary_prompt
from text_splitter import split_text
from embeddings import get_embedding_model
from vector_store import create_vector_store
from retriever import retrieve_documents
from prompt import build_chat_prompt
from risk_detector import build_risk_prompt
from memory import get_memory
from clause_classifier import classify_clause

# LOAD EMBEDDING MODEL ONLY ONCE
@st.cache_resource
def load_embeddings():
    return get_embedding_model()

embedding_model = load_embeddings()

st.set_page_config(
    page_title="Legal RAG Assistant",
    page_icon="⚖️",
    layout="wide"
)
st.markdown("""
<div style='margin-bottom:25px'>
<h1>⚖️ Legal AI Assistant</h1>
<p style='font-size:18px;color:#94A3B8'>
Analyze contracts, detect risks, generate summaries and perform semantic legal search using AI.
</p>
</div>
""", unsafe_allow_html=True)

# CUSTOM UI STYLING
st.markdown("""
<style>

/* Main App */
.stApp {
    background: linear-gradient(135deg, #0B1120 0%, #0F172A 100%);
    color: white;
}

/* Text */
h1, h2, h3, h4, h5, h6, p, label {
    color: white !important;
}

/* Main Header */
h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #60A5FA, #34D399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Upload Box */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05);
    border: 2px dashed #3B82F6;
    border-radius: 18px;
    padding: 20px;
    backdrop-filter: blur(10px);
}

[data-testid="stFileUploader"]:hover {
    border-color: #60A5FA;
    box-shadow: 0 0 20px rgba(59,130,246,0.4);
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 14px;
    height: 3.2em;
    border: none;
    font-size: 16px;
    font-weight: 700;
    background: linear-gradient(90deg, #2563EB, #3B82F6);
    color: white;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(37,99,235,0.4);
}

/* Chat Messages */
.stChatMessage {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
    backdrop-filter: blur(10px);
}

/* Input Box */
.stTextInput input {
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
}

/* Cards */
div[data-testid="stVerticalBlock"] > div:has(.element-container) {
    border-radius: 18px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #3B82F6;
    border-radius: 20px;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.markdown("""
# ⚖️ Legal AI

### 🚀 Features

✅ Legal Q&A

✅ Risk Detection

✅ Contract Summarization

✅ Semantic Search

---

### 🛠 Tech Stack

• FastAPI

• LangChain

• ChromaDB

• Groq LLM

• Streamlit

---

### 💡 Tip

Upload a legal PDF and ask:
> "Summarize this agreement"

> "Identify risky clauses"

> "What is the termination notice period?"
""")

# SESSION STATE INITIALIZATION
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None   

if "memory" not in st.session_state:
    st.session_state.memory = get_memory()

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file:

    if st.session_state.current_pdf != uploaded_file.name:
        st.session_state.messages = []
        st.session_state.memory = get_memory()
        st.session_state.current_pdf = uploaded_file.name

if uploaded_file:

    os.makedirs("../data/legal_docs", exist_ok=True)

    save_path = os.path.join(
        "../data/legal_docs",
        uploaded_file.name
    )

    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    def process_document(file_path):

        loader = PyPDFLoader(file_path)

        pages = loader.load()

        chunks = split_text(pages)

        unique_db_path = None

        vector_store = create_vector_store(
            chunks,
            embedding_model,
            persist_directory=unique_db_path
        )

        return pages, chunks, vector_store

    pages, chunks, vector_store = process_document(save_path)
    col1, col2, col3 = st.columns(3)
    col1.metric("Pages", len(pages))
    col2.metric("Chunks", len(chunks))
    col3.metric("AI Status", "Ready")

    st.success("AI system ready!")
    st.sidebar.subheader("PDF Preview")
    st.divider()

    # TABS
    tab1, tab2, tab3, tab4, tab5= st.tabs(
    [
        "💬 Legal Chat",
        "⚠️ Risk Analysis",
        "📝 Document Summary",
        "📑 Clause Extraction",
        "⚖️ Contract Comparison"
    ]
)

    # ==========================================
    # TAB 1: CHAT
    # ==========================================
    with tab1:
        st.subheader("Legal AI Assistant")

        # Display conversation history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Text Input Component
        chat_query = st.chat_input("Ask a legal question", key="legal_chat_input")
        
        # Determine the active query source
        query = chat_query

        if query and query.strip() != "":
            # Display user query instantly
            with st.chat_message("user"):
                st.markdown(query)

            st.session_state.messages.append({"role": "user", "content": query})

            # RAG Pipeline execution
            results = retrieve_documents(vector_store, query)
            context = "\n\n".join([doc.page_content for doc in results])
            prompt = build_chat_prompt(context, query)

            with st.spinner("Thinking..."):
                try:
                    api_response = requests.post(
    "https://legal-rag-assistant-2-hbcr.onrender.com/chat",
    json={"question": prompt},
    timeout=120
)
                    # FIXED: Changed from raise_for_error() to raise_for_status()
                    api_response.raise_for_status() 
                    response = api_response.json().get("response", "No clear answer received.")
                except Exception as e:
                    response = f"⚠️ Backend Connection Error: {str(e)}"

            # Save to conversation memory
            st.session_state.memory.add_user_message(query)
            st.session_state.memory.add_ai_message(response)

            # Display response using proper wrapping layout
            with st.chat_message("assistant"):
                st.markdown(response)
                
            st.session_state.messages.append({"role": "assistant", "content": response})

            st.divider()

            # Source Citations UI Setup
            st.subheader("Sources & References")
            for i, doc in enumerate(results):
                categories = classify_clause(doc.page_content)
                page_num = doc.metadata.get('page', 0) + 1
                
                with st.expander(f"Source {i+1} — Page {page_num}"):
                    if categories:
                        st.markdown(f"**Identified Classifications:** `{', '.join(categories)}`")
                    st.write(doc.page_content)

    # ==========================================
    # TAB 2: RISK ANALYSIS
    # ==========================================
    with tab2:
        st.subheader("AI Risk Analysis")

        if st.button("Analyze Risks"):
            context = "\n\n".join([doc.page_content for doc in chunks[:3]])
            risk_prompt = build_risk_prompt(context)

            with st.spinner("Analyzing risks..."):
                try:
                     api_response = requests.post(
    "https://legal-rag-assistant-2-hbcr.onrender.com/chat",
                    json={"question": risk_prompt},
                    timeout=120)
                     risk_response = api_response.json()["response"]
                     st.markdown(risk_response)
                except Exception as e:
                    st.error(f"Failed to communicate with API: {e}")
    # ==========================================
    # TAB 3: SUMMARY
    # ==========================================
    with tab3:
        st.subheader("AI Document Summary")

        if st.button("Summarize Document"):
            context = "\n\n".join([doc.page_content for doc in chunks[:3]])
            summary_prompt = build_summary_prompt(context)

            with st.spinner("Generating summary..."):
                try:
                    api_response = requests.post(
    "https://legal-rag-assistant-2-hbcr.onrender.com/chat",
    json={"question": summary_prompt},
    timeout=120
)
                    summary_response = api_response.json()["response"]
                    st.markdown(summary_response)
                except Exception as e:
                    st.error(f"Failed to communicate with API: {e}")


    # ==========================================
    # TAB 5: CLAUSE EXTRACTION
    # ==========================================
    with tab4:
        st.subheader("Clause Extraction")

        clause_type = st.selectbox(
            "Select Clause Type",
            ["Termination", "Confidentiality", "Liability", "Indemnity", "Non-Compete"]
        )

        if st.button("Extract Clauses"):
            extracted_clauses = []

            for doc in chunks:
                if clause_type.lower() in doc.page_content.lower():
                    extracted_clauses.append(doc.page_content)

            if extracted_clauses:
                st.success(f"Found {len(extracted_clauses)} matching clauses")
                for i, clause in enumerate(extracted_clauses):
                    with st.expander(f"{clause_type} Clause {i+1}"):
                        st.write(clause)
            else:
                st.warning("No matching clauses found.")
        # ==========================================
    # TAB 6: CONTRACT COMPARISON
    # ==========================================
        # ==========================================
    # TAB 6: CONTRACT COMPARISON
    # ==========================================
    with tab5:

        st.subheader("Compare Two Contracts")

        contract1 = st.file_uploader(
            "Upload Contract A",
            type="pdf",
            key="contract_a"
        )

        contract2 = st.file_uploader(
            "Upload Contract B",
            type="pdf",
            key="contract_b"
        )

        if contract1 and contract2:

            if st.button("Compare Contracts"):

                with st.spinner("Analyzing contracts..."):

                    try:

                        # Save contract A
                        contract1_path = os.path.join(
                            "../data/legal_docs",
                            contract1.name
                        )

                        with open(contract1_path, "wb") as f:
                            f.write(contract1.read())

                        # Save contract B
                        contract2_path = os.path.join(
                            "../data/legal_docs",
                            contract2.name
                        )

                        with open(contract2_path, "wb") as f:
                            f.write(contract2.read())

                        # Load PDFs
                        loader1 = PyPDFLoader(contract1_path)
                        loader2 = PyPDFLoader(contract2_path)

                        docs1 = loader1.load()
                        docs2 = loader2.load()

                        # Extract text
                        text1 = "\n".join(
                            [doc.page_content for doc in docs1]
                        )

                        text2 = "\n".join(
                            [doc.page_content for doc in docs2]
                        )

                        comparison_prompt = f"""
Compare these two legal contracts.

CONTRACT A:
{text1[:12000]}

CONTRACT B:
{text2[:12000]}

Analyze:
- key similarities
- key differences
- compensation changes
- termination clause differences
- confidentiality differences
- risk analysis
- missing clauses
- legal concerns

Provide clean bullet points.
"""

                        api_response = requests.post(
                             "https://legal-rag-assistant-2-hbcr.onrender.com/chat",
                            json={"question": comparison_prompt}
                        )

                        comparison_result = api_response.json()["response"]

                        st.success("Comparison Complete")

                        st.markdown(comparison_result)

                    except Exception as e:

                        st.error(f"Comparison failed: {e}")

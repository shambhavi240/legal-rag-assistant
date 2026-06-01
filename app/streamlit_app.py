import os
import uuid
import re
import base64
import requests
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
import shutil
# Custom module imports
from risk_score import build_risk_score_prompt
from summarizer import build_summary_prompt
from text_splitter import split_text
from embeddings import get_embedding_model
from vector_store import create_vector_store
from retriever import retrieve_documents
from prompt import build_prompt
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

# CUSTOM UI STYLING
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0F172A;
        color: white;
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: white !important;
    }

    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown span {
        color: white !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .stButton button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background: linear-gradient(90deg, #2563EB, #1D4ED8);
        color: white;
        border: none;
        font-size: 16px;
        font-weight: bold;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #1D4ED8, #1E40AF);
        color: white;
    }

    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        background-color: #1E293B;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# SIDEBAR
st.sidebar.markdown(
    """
    # ⚖️ Legal AI Dashboard

    ### Features

    ✅ Legal Q&A

    ✅ Risk Analysis

    ✅ Document Summarization

    ✅ Semantic Search

    ---

    Built using:

    - FastAPI
    - LangChain
    - ChromaDB
    - Groq LLM
    """
)

# SESSION STATE INITIALIZATION
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memory" not in st.session_state:
    st.session_state.memory = get_memory()

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

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

        unique_db_path = f"./chroma_db_{uuid.uuid4()}"

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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "💬 Legal Chat",
        "⚠️ Risk Analysis",
        "📝 Document Summary",
        "📊 Risk Scoring",
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
            prompt = build_prompt(context, query)

            with st.spinner("Thinking..."):
                try:
                    api_response = requests.post(
                        requests.post(
                            "https://legal-rag-assistant-h7k0.onrender.com/chat",
                        json={"question": prompt},
                        timeout=30
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
                        "https://legal-rag-assistant-h7k0.onrender.com/chat",
                        json={"question": risk_prompt}
                    )
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
                        "http://127.0.0.1:8000/chat",
                        json={"question": summary_prompt}
                    )
                    summary_response = api_response.json()["response"]
                    st.markdown(summary_response)
                except Exception as e:
                    st.error(f"Failed to communicate with API: {e}")

    # ==========================================
    # TAB 4: RISK SCORING
    # ==========================================
    with tab4:
        st.subheader("AI Risk Scoring")

        if st.button("Generate Risk Score"):
            context = "\n\n".join([doc.page_content for doc in chunks[:3]])
            text = context.lower()

            risk_score = 0
            risks = []

            # Rule-based processing logic
            if "unlimited liability" in text:
                risk_score += 3
                risks.append("Unlimited liability clause detected")
            if "termination" not in text:
                risk_score += 2
                risks.append("Termination clause missing")
            if "confidentiality" not in text:
                risk_score += 1
                risks.append("Confidentiality clause missing")
            if "indemnify" in text:
                risk_score += 2
                risks.append("Indemnity obligations detected")
            if "arbitration" not in text:
                risk_score += 1
                risks.append("Dispute resolution clause missing")

            risk_score = min(risk_score, 10)
            risk_score_prompt = build_risk_score_prompt(context)

            with st.spinner("Calculating risk score..."):
                try:
                    api_response = requests.post(
                        "http://127.0.0.1:8000/chat",
                        json={"question": risk_score_prompt}
                    )
                    risk_score_response = api_response.json()["response"]
                except Exception as e:
                    risk_score_response = f"Failed to get AI evaluation: {e}"

            st.write(f"### Risk Score: {risk_score}/10")

            if risks:
                st.write("### Detected Risks")
                for risk in risks:
                    st.write(f"- {risk}")

            st.divider()
            st.markdown(risk_score_response)

    # ==========================================
    # TAB 5: CLAUSE EXTRACTION
    # ==========================================
    with tab5:
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
    with tab6:

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
                            "http://127.0.0.1:8000/chat",
                            json={"question": comparison_prompt}
                        )

                        comparison_result = api_response.json()["response"]

                        st.success("Comparison Complete")

                        st.markdown(comparison_result)

                    except Exception as e:

                        st.error(f"Comparison failed: {e}")
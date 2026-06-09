# ⚖️ Legal RAG Assistant
# Live Application:
https://your-streamlit-app.streamlit.app

## Overview

Legal RAG Assistant is an AI-powered application designed to analyze, summarize, compare, and identify risks in legal documents using Retrieval-Augmented Generation (RAG). The system combines document retrieval with Large Language Models (LLMs) to provide context-aware legal insights.

The project enables users to upload legal documents and interact with them through natural language queries, making legal document analysis faster and more accessible.

---

## Features

### 📄 Document Upload and Processing

* Upload PDF legal documents.
* Automatic text extraction and preprocessing.
* Intelligent document chunking for efficient retrieval.

### 🔍 Retrieval-Augmented Generation (RAG)

* Semantic search using vector embeddings.
* Context-aware document retrieval.
* Accurate responses grounded in uploaded documents.

### 💬 Legal Question Answering

* Ask questions about uploaded legal documents.
* Receive answers based on retrieved document context.

### 📝 Document Summarization

* Generate concise summaries of lengthy legal documents.
* Highlight important clauses and provisions.

### ⚠️ Risk Detection

* Identify potentially risky clauses.
* Highlight obligations, liabilities, and restrictive terms.

### 📑 Clause Classification

* Categorize legal clauses automatically.
* Improve contract understanding and review efficiency.

### 🔄 Document Comparison

* Compare legal documents and identify key differences.

---

## System Architecture

User → Streamlit Frontend → FastAPI Backend → RAG Pipeline → LLM Response

### Workflow

1. User uploads a legal document.
2. Text is extracted from the PDF.
3. Document is split into chunks.
4. Embeddings are generated for each chunk.
5. Chunks are stored in a vector database.
6. Relevant chunks are retrieved based on user queries.
7. Retrieved context is combined with the query.
8. The LLM generates a context-aware response.

---

## Technologies Used

### Frontend

* Streamlit

### Backend

* FastAPI
* Uvicorn

### AI & RAG

* LangChain
* Sentence Transformers
* FAISS
* Transformers

### Document Processing

* PyPDF
* PDF Loaders

### Programming Language

* Python

---

## Project Structure

```text
legal-rag-assistant/
│
├── app/
│   ├── streamlit_app.py
│   ├── prompt.py
│   ├── summarizer.py
│   ├── retriever.py
│   ├── vector_store.py
│   ├── embeddings.py
│   ├── memory.py
│   ├── clause_classifier.py
│   └── risk_detector.py
│
├── backend/
│   └── API files
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Deployment

### Frontend

Streamlit Cloud

### Backend

Render

### API Documentation

```text
https://legal-rag-assistant-2-hbcr.onrender.com/docs
```

### Backend URL

```text
https://legal-rag-assistant-2-hbcr.onrender.com

### Frontend
```text
https://github.com/shambhavi240/legal-rag-assistant
```

---

## API Endpoints

### Chat

```http
POST /chat
```

### Summary

```http
POST /summary
```

### Risk Analysis

```http
POST /risk
```

### Clause Classification

```http
POST /clauses
```

### Document Comparison

```http
POST /compare
```

---

## Sample Query

**Question**

```text
What is the retirement date mentioned in the agreement?
```

**Answer**

```text
The executive's retirement date is March 31, 2023.
```

---

## Future Enhancements

* Multi-document querying
* Legal citation generation
* Advanced clause extraction
* Multilingual legal document support
* Agentic AI-based contract review
* Fine-tuned legal LLM integration

---

## Author

Siddhi Shahi

Computer Science Engineering Student

Project: Legal Document Summarization with Fine-Tuned LLM and Retrieval-Augmented Generation (RAG)

---

## License

This project is developed for educational and research purposes.

from langchain_community.document_loaders import PyPDFLoader

from text_splitter import split_text

from embeddings import get_embedding_model

from vector_store import create_vector_store

from retriever import retrieve_documents

from llm import get_llm

from prompt import build_prompt


loader = PyPDFLoader("../sample.pdf")

pages = loader.load()


chunks = split_text(pages)


embedding_model = get_embedding_model()


vector_store = create_vector_store(
    chunks,
    embedding_model
)


query = "What is the termination clause?"


results = retrieve_documents(
    vector_store,
    query
)


context = "\n\n".join(
    [doc.page_content for doc in results]
)


prompt = build_prompt(
    context,
    query
)


llm = get_llm()


response = llm.invoke(prompt)


print("\nAI RESPONSE:\n")

print(response.content)
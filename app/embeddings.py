import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings


@st.cache_resource
def get_embedding_model():

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    return embeddings
import os

import streamlit as st

from dotenv import load_dotenv

from langchain_groq import ChatGroq


load_dotenv()


@st.cache_resource
def get_llm():

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    
    )

    return llm
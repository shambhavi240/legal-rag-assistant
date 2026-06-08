import os
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
def get_llm():

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    
    )

    return llm

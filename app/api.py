from fastapi import FastAPI

from pydantic import BaseModel

from app.llm import get_llm


app = FastAPI()


llm = get_llm()


class ChatRequest(BaseModel):

    question: str


@app.get("/home")
def home():

    return {
        "message": "Legal RAG API Running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    response = llm.invoke(
        request.question
    )

    return {
        "response": response.content
    }
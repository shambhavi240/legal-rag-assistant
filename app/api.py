from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import get_llm

from app.prompt import (
    build_chat_prompt,
    build_summary_prompt,
    build_risk_prompt,
    build_clause_prompt,
    build_comparison_prompt
)

app = FastAPI()

llm = get_llm()


class ChatRequest(BaseModel):
    question: str


class DocumentRequest(BaseModel):
    document: str


class CompareRequest(BaseModel):
    contract1: str
    contract2: str


@app.get("/")
def root():
    return {"message": "Legal RAG Backend Running"}


@app.get("/home")
def home():
    return {"message": "Legal RAG API Running"}


@app.post("/chat")
def chat(request: ChatRequest):

    response = llm.invoke(request.question)

    return {
        "response": response.content
    }


@app.post("/summary")
def summary(request: DocumentRequest):

    prompt = build_summary_prompt(
        request.document
    )

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


@app.post("/risk")
def risk(request: DocumentRequest):

    prompt = build_risk_prompt(
        request.document
    )

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


@app.post("/clauses")
def clauses(request: DocumentRequest):

    prompt = build_clause_prompt(
        request.document
    )

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }


@app.post("/compare")
def compare(request: CompareRequest):

    prompt = build_comparison_prompt(
        request.contract1,
        request.contract2
    )

    response = llm.invoke(prompt)

    return {
        "response": response.content
    }

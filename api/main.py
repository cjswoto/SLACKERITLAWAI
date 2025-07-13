from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

from slacker_ai_suite.chat_manager import ConversationManager
from slacker_ai_suite.knowledge_base import KnowledgeBase

app = FastAPI(title="Slacker AI Suite")

kb = KnowledgeBase(Path("kb_store"))
chat_manager = ConversationManager(kb=kb)


@app.get("/health")
def health():
    return {"status": "ok"}


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    response = chat_manager.chat(req.session_id, req.message)
    return {"response": response}


class KBAddRequest(BaseModel):
    texts: list[str]


@app.post("/kb/add")
def kb_add(req: KBAddRequest):
    kb.add_texts(req.texts)
    return {"count": len(req.texts)}


class KBQueryRequest(BaseModel):
    query: str
    top_k: int = 3


@app.post("/kb/search")
def kb_search(req: KBQueryRequest):
    return {"results": kb.search(req.query, req.top_k)}

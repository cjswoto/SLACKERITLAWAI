from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .ollama_client import OllamaClient
from .knowledge_base import KnowledgeBase


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ChatSession:
    messages: List[Message] = field(default_factory=list)


class ConversationManager:
    def __init__(self, kb: KnowledgeBase | None = None, model: str = "llama2"):
        self.sessions: dict[str, ChatSession] = {}
        self.kb = kb
        self.model = model
        self.client = OllamaClient()

    def chat(self, session_id: str, user_message: str) -> str:
        session = self.sessions.setdefault(session_id, ChatSession())
        session.messages.append(Message("user", user_message))
        context = "\n".join(m.content for m in session.messages[-5:])
        if self.kb:
            kb_snippets = self.kb.search(user_message)
            if kb_snippets:
                context += "\n" + "\n".join(kb_snippets)
        response = self.client.generate_completion(context, self.model)
        session.messages.append(Message("assistant", response))
        return response

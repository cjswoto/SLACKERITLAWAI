from __future__ import annotations

from pathlib import Path
from typing import Iterable
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class KnowledgeBase:
    """Simple vectorizer-based knowledge base without external dependencies."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.meta_file = self.storage_path / "kb_texts.json"
        self.texts: list[str] = []
        self.vectorizer = TfidfVectorizer()
        self.vectors = None
        if self.meta_file.exists():
            self.texts = json.loads(self.meta_file.read_text())
            if self.texts:
                self.vectors = self.vectorizer.fit_transform(self.texts)

    def _save(self):
        self.meta_file.write_text(json.dumps(self.texts))

    def add_texts(self, texts: Iterable[str]):
        self.texts.extend(list(texts))
        self.vectors = self.vectorizer.fit_transform(self.texts)
        self._save()

    def search(self, query: str, top_k: int = 3) -> list[str]:
        if not self.texts:
            return []
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.vectors)[0]
        top_indices = sims.argsort()[::-1][:top_k]
        return [self.texts[i] for i in top_indices]

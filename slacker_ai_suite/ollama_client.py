import os
import requests


class OllamaClient:
    """Minimal client for interacting with a local Ollama server."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.session = requests.Session()

    def list_models(self) -> list[str]:
        try:
            r = self.session.get(f"{self.base_url}/api/tags")
            r.raise_for_status()
            data = r.json()
            return [m.get("name") for m in data.get("models", [])]
        except Exception:
            return []

    def generate_completion(self, prompt: str, model: str) -> str:
        payload = {"model": model, "prompt": prompt}
        try:
            r = self.session.post(f"{self.base_url}/api/generate", json=payload, timeout=30)
            r.raise_for_status()
            return r.json().get("response", "")
        except Exception:
            # In tests or offline scenarios we just return a stub
            return "(no response)"

"""
LexIQ Labs – Response History

Purpose:
- Store and retrieve past responses within a session
- Support collapsible UI history (customer input + final response only)
- Lightweight, in-memory by default
"""

from typing import List, Dict
from datetime import datetime
import uuid


class ResponseHistory:
    def __init__(self):
        self._history: List[Dict] = []

    def add(
        self,
        *,
        customer_message: str,
        final_response: str,
        persona: str,
    ) -> Dict:
        entry = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.utcnow().isoformat(),
            "persona": persona,
            "customer_message": customer_message.strip(),
            "final_response": final_response.strip(),
            "title": self._generate_title(customer_message),
        }
        self._history.insert(0, entry)  # newest first
        return entry

    def list(self) -> List[Dict]:
        """
        Return all history entries (newest first).
        """
        return self._history

    def get(self, entry_id: str) -> Dict | None:
        for entry in self._history:
            if entry["id"] == entry_id:
                return entry
        return None

    def clear(self) -> None:
        self._history.clear()

    def _generate_title(self, customer_message: str) -> str:
        """
        Generate a short, human-readable title from the customer message.
        """
        text = customer_message.strip().splitlines()[0]
        words = text.split()
        if len(words) <= 8:
            return text
        return " ".join(words[:8]) + "…"

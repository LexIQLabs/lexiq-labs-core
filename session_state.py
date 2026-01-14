"""
LexIQ Labs – Session State

Purpose:
- Maintain per-session context
- Store persona, voice profile, settings, and response history
- Lightweight, in-memory implementation (backend-agnostic)
"""

from typing import Dict, Optional
from datetime import datetime
import uuid

from response_history import ResponseHistory


class SessionState:
    def __init__(self):
        self.session_id: str = str(uuid.uuid4())
        self.created_at: str = datetime.utcnow().isoformat()

        # Session-level selections
        self.persona: Optional[str] = None
        self.voice_profile: Optional[Dict] = None

        # Settings
        self.settings: Dict = {
            "tone_mode": "auto",      # auto | conservative | assertive
            "gemini_enabled": True,   # can be toggled
        }

        # Runtime state
        self.response_history = ResponseHistory()

    # -------- Persona --------

    def set_persona(self, persona: str) -> None:
        self.persona = persona

    def get_persona(self) -> Optional[str]:
        return self.persona

    # -------- Voice Profile --------

    def set_voice_profile(self, voice_profile: Dict) -> None:
        self.voice_profile = voice_profile

    def get_voice_profile(self) -> Optional[Dict]:
        return self.voice_profile

    def clear_voice_profile(self) -> None:
        self.voice_profile = None

    # -------- Settings --------

    def update_settings(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if key in self.settings:
                self.settings[key] = value

    def get_settings(self) -> Dict:
        return self.settings

    # -------- Response History --------

    def add_response(
        self,
        *,
        customer_message: str,
        final_response: str,
    ) -> Dict:
        if not self.persona:
            raise ValueError("Persona must be set before adding responses.")

        return self.response_history.add(
            customer_message=customer_message,
            final_response=final_response,
            persona=self.persona,
        )

    def list_responses(self):
        return self.response_history.list()

    def get_response(self, entry_id: str):
        return self.response_history.get(entry_id)

    def clear_responses(self):
        self.response_history.clear()

import reflex as rx
from typing import List, TypedDict
from datetime import datetime


class Session(TypedDict):
    date: str
    type: str
    preview: str


class SessionState(rx.State):
    """State to manage saved chat and narrative sessions."""

    sessions: List[Session] = [
        {
            "date": "2023-10-27",
            "type": "EMS",
            "preview": "Patient with chest pain...",
        },
        {
            "date": "2023-10-26",
            "type": "Fire",
            "preview": "Structure fire, single family...",
        },
        {
            "date": "2023-10-25",
            "type": "Both",
            "preview": "MVA with entrapment...",
        },
    ]

    @rx.event
    async def select_session(self, session_date: str):
        """Placeholder for selecting a session."""
        print(f"Selected session: {session_date}")

    @rx.event
    async def add_session(
        self, session_type: str, preview_text: str
    ):
        """Add a new session to the list."""
        new_session: Session = {
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            "type": session_type,
            "preview": preview_text,
        }
        self.sessions.insert(0, new_session)

    @rx.event
    async def open_settings(self):
        """Placeholder for opening settings."""
        print("Opening settings")
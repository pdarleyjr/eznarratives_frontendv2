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
            "date": "2023-10-27 10:30",
            "type": "EMS",
            "preview": "Patient with chest pain, possible MI, transported...",
        },
        {
            "date": "2023-10-26 15:00",
            "type": "Fire",
            "preview": "Structure fire, single family dwelling, extinguished...",
        },
        {
            "date": "2023-10-25 08:15",
            "type": "Both",
            "preview": "MVA with entrapment, extrication required, pt transported...",
        },
        {
            "date": "2023-10-24 12:00",
            "type": "Chat",
            "preview": "User asked about protocols for stroke assessment...",
        },
    ]

    @rx.event
    async def select_session(self, session_date: str):
        """Loads the selected session's data (placeholder)."""
        print(f"Selected session: {session_date}")
        from app.states.ui_state import UiState

        ui_state = await self.get_state(UiState)
        ui_state.set_active_session(session_date)

    @rx.event
    async def add_session(
        self, session_type: str, preview_text: str
    ):
        """Add a new session to the list."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_session: Session = {
            "date": now_str,
            "type": session_type,
            "preview": preview_text,
        }
        if (
            not self.sessions
            or self.sessions[0]["preview"] != preview_text
        ):
            self.sessions.insert(0, new_session)
            from app.states.ui_state import UiState

            ui_state = await self.get_state(UiState)
            ui_state.set_active_session(now_str)

    @rx.event
    async def open_settings(self):
        """Placeholder for opening settings."""
        print("Opening settings")
        from app.states.ui_state import UiState

        ui_state = await self.get_state(UiState)
        ui_state.set_active_session(None)
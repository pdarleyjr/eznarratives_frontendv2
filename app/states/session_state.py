import reflex as rx
from typing import List, TypedDict
from datetime import datetime
from app.states.ui_state import UiState


class Session(TypedDict):
    date: str
    type: str
    preview: str


class SessionState(rx.State):
    """State to manage saved chat and narrative sessions."""

    sessions: List[Session] = [
        {
            "date": "2023-10-27T10:30:00",
            "type": "EMS",
            "preview": "Patient with chest pain, possible MI, transported...",
        },
        {
            "date": "2023-10-26T15:00:00",
            "type": "Fire",
            "preview": "Structure fire, single family dwelling, extinguished...",
        },
        {
            "date": "2023-10-25T08:15:00",
            "type": "Both",
            "preview": "MVA with entrapment, extrication required, pt transported...",
        },
        {
            "date": "2023-10-24T12:00:00",
            "type": "Chat",
            "preview": "User asked about protocols for stroke assessment...",
        },
    ]

    @rx.event
    async def select_session(self, session_date: str):
        """Loads the selected session's data (placeholder for now)."""
        print(f"Selected session: {session_date}")
        ui_state = await self.get_state(UiState)
        ui_state.set_active_session(session_date)

    @rx.event
    async def add_session(
        self, session_type: str, preview_text: str
    ):
        """Add a new session to the list, ensuring no exact duplicates."""
        now_iso = datetime.now().isoformat(
            timespec="seconds"
        )
        new_session: Session = {
            "date": now_iso,
            "type": session_type,
            "preview": preview_text,
        }
        if (
            not self.sessions
            or self.sessions[0]["preview"] != preview_text
            or self.sessions[0]["type"] != session_type
        ):
            async with self:
                self.sessions.insert(0, new_session)
            ui_state = await self.get_state(UiState)
            ui_state.set_active_session(now_iso)

    @rx.event
    async def open_settings(self):
        """Placeholder action for opening settings."""
        print("Opening settings (Placeholder)")
        yield rx.toast.info(
            "Settings page not implemented yet.",
            position="top-center",
        )
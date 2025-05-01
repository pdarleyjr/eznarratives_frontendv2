import reflex as rx
from typing import List, Dict, TypedDict
import asyncio
import os


class Message(TypedDict):
    text: str
    is_ai: bool


class ChatState(rx.State):
    """State for the chat interface."""

    messages: List[Message] = []
    typing: bool = False
    processing: bool = False

    @rx.event
    def clear_messages(self):
        """Clear the chat history."""
        self.messages = []

    @rx.event
    async def send_message(self, form_data: Dict[str, str]):
        """Send a message and get a response."""
        text = form_data.get("message")
        if not text:
            return
        async with self:
            self.messages.append(
                {"text": text, "is_ai": False}
            )
            self.typing = True
            self.processing = True
        yield
        await asyncio.sleep(1)
        async with self:
            self.messages.append(
                {"text": f"Echo: {text}", "is_ai": True}
            )
            self.typing = False
            self.processing = False
        yield
        from app.states.session_state import SessionState

        session_state = await self.get_state(SessionState)
        await session_state.add_session(
            "Chat", text[:50] + "..."
        )

    @rx.event
    async def send_preset_message(self, text: str):
        """Send a preset message."""
        if not text:
            return
        async with self:
            self.messages.append(
                {"text": text, "is_ai": False}
            )
            self.typing = True
            self.processing = True
        yield
        await asyncio.sleep(1)
        async with self:
            self.messages.append(
                {
                    "text": f"Responding to: {text}",
                    "is_ai": True,
                }
            )
            self.typing = False
            self.processing = False
        yield
        from app.states.session_state import SessionState

        session_state = await self.get_state(SessionState)
        await session_state.add_session(
            "Chat", text[:50] + "..."
        )

    @rx.event
    def cancel_typing(self):
        """Cancel AI typing/processing."""
        self.typing = False
        self.processing = False
import reflex as rx
from typing import List, Dict, TypedDict
import asyncio
import os
from app.states.session_state import SessionState


class Message(TypedDict):
    text: str
    is_ai: bool


class ChatState(rx.State):
    """State for the chat interface."""

    messages: List[Message] = []
    typing: bool = False
    processing: bool = False
    current_message: str = ""

    @rx.event
    def clear_messages(self):
        """Clear the chat history."""
        self.messages = []
        self.current_message = ""

    @rx.event
    async def send_message(self, form_data: Dict[str, str]):
        """Send a message and get a response."""
        text = self.current_message.strip()
        if not text or self.processing:
            return
        self.current_message = ""
        async with self:
            self.messages.append(
                {"text": text, "is_ai": False}
            )
            self.typing = True
            self.processing = True
        yield
        await asyncio.sleep(1.5)
        if not self.processing:
            return
        async with self:
            self.messages.append(
                {"text": f"Echo: {text}", "is_ai": True}
            )
            self.typing = False
            self.processing = False
        yield
        session_state = await self.get_state(SessionState)
        await session_state.add_session(
            "Chat",
            text[:50] + ("..." if len(text) > 50 else ""),
        )

    @rx.event
    async def send_preset_message(self, text: str):
        """Send a preset message."""
        if not text or self.processing:
            return
        self.current_message = ""
        async with self:
            self.messages.append(
                {"text": text, "is_ai": False}
            )
            self.typing = True
            self.processing = True
        yield
        await asyncio.sleep(1)
        if not self.processing:
            return
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
        session_state = await self.get_state(SessionState)
        await session_state.add_session(
            "Chat",
            text[:50] + ("..." if len(text) > 50 else ""),
        )

    @rx.event
    def cancel_typing(self):
        """Cancel AI typing/processing."""
        if self.processing:
            self.typing = False
            self.processing = False
            yield rx.toast.info(
                "Processing cancelled.",
                duration=2000,
                position="top-center",
            )

    @rx.event
    def set_current_message(self, value: str):
        """Update the current message in the input field."""
        self.current_message = value
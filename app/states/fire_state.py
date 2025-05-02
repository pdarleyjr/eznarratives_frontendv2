import reflex as rx
from typing import Dict, List, Any, TypedDict
from app.states.session_state import SessionState


class FireState(rx.State):
    """State for the Fire report form."""

    fire_narrative: str = ""
    unit: str = ""
    emergency_type: str = "Structure Fire"
    emergency_types: List[str] = [
        "Structure Fire",
        "Vehicle Fire",
        "Wildfire",
        "Medical Assist",
        "Hazardous Materials",
        "Service Call",
        "Alarm Activation",
        "Other",
    ]
    additional_information: str = ""

    @rx.event
    async def generate_narrative(self):
        """Generate narrative from Fire data."""
        print("Generating Fire narrative...")
        narrative = f"Unit {self.unit or '[Unit]'}"
        narrative += f" responded to a report of {self.emergency_type or '[Emergency]'}. "
        if self.additional_information:
            narrative += f"Additional details: {self.additional_information}."
        else:
            narrative += "Situation addressed as per standard procedures."
        async with self:
            self.fire_narrative = narrative.strip()
        yield rx.toast.success(
            "Fire narrative generated!",
            duration=2000,
            position="top-center",
        )
        narrative_preview = self.fire_narrative[:50] + (
            "..." if len(self.fire_narrative) > 50 else ""
        )
        session_state = await self.get_state(SessionState)
        await session_state.add_session(
            "Fire", narrative_preview
        )

    @rx.event
    def set_unit(self, value: str):
        self.unit = value

    @rx.event
    def set_emergency_type(self, value: str):
        self.emergency_type = value

    @rx.event
    def set_additional_information(self, value: str):
        self.additional_information = value
import reflex as rx
from typing import Dict, List, Any, TypedDict


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
        "Other",
    ]
    additional_information: str = ""

    @rx.event
    async def generate_narrative(self):
        """Generate narrative from Fire data."""
        print("Generating Fire narrative...")
        narrative = f"Unit {self.unit} responded to a {self.emergency_type}. "
        if self.additional_information:
            narrative += f"Additional info: {self.additional_information}."
        else:
            narrative += (
                "No additional information provided."
            )
        self.fire_narrative = narrative
        narrative_preview = narrative[:50] + "..."
        from app.states.session_state import SessionState

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
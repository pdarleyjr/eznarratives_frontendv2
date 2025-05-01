import reflex as rx
from typing import Dict, List, Any, TypedDict


class EmsState(rx.State):
    """State for the EMS report form."""

    active_ems_section: str = "Dispatch"
    ems_narrative: str = ""
    unit: str = ""
    dispatch_reason: str = "Medical"
    dispatch_reasons: List[str] = [
        "Medical",
        "Trauma",
        "Fire Call",
        "Other",
    ]
    response_delay: str = "None"
    response_delays: List[str] = [
        "None",
        "< 5 min",
        "5-15 min",
        "> 15 min",
    ]
    patient_presentation: str = ""
    chief_complaint: str = ""
    opqrst_data: Dict[str, str] = {
        "onset": "",
        "provocation": "",
        "quality": "",
        "radiation": "",
        "severity": "",
        "time": "",
    }
    vitals_wnl: bool = True
    bp_systolic: int = 0
    bp_diastolic: int = 0
    hr: int = 0
    rr: int = 0
    level_of_consciousness: str = "Alert"
    consciousness_levels: List[str] = [
        "Alert",
        "Verbal",
        "Pain",
        "Unresponsive",
    ]
    protocol_selection: List[str] = []
    protocols: List[str] = [
        "Cardiac Arrest",
        "Stroke",
        "Trauma",
        "Allergic Reaction",
        "Seizure",
    ]
    interventions: List[str] = []
    all_interventions: List[str] = [
        "IV Establishment",
        "Oxygen Administration",
        "Medication Administration",
        "Airway Management",
    ]
    medications_given: List[Dict[str, str | int]] = []
    destination_facility: str = ""
    transport_mode: str = "ALS"
    transport_modes: List[str] = ["ALS", "BLS"]
    room_number: str = ""
    receiving_staff: str = ""

    @rx.event
    def set_active_ems_section(self, section: str):
        """Set the active EMS form section."""
        self.active_ems_section = section

    @rx.event
    def toggle_protocol(self, protocol: str, checked: bool):
        """Add or remove a protocol from the selection."""
        if checked:
            if protocol not in self.protocol_selection:
                self.protocol_selection.append(protocol)
        elif protocol in self.protocol_selection:
            self.protocol_selection.remove(protocol)
        self.protocol_selection = sorted(
            self.protocol_selection
        )

    @rx.event
    def toggle_intervention(
        self, intervention: str, checked: bool
    ):
        """Add or remove an intervention from the list."""
        if checked:
            if intervention not in self.interventions:
                self.interventions.append(intervention)
        elif intervention in self.interventions:
            self.interventions.remove(intervention)
        self.interventions = sorted(self.interventions)

    @rx.event
    def add_medication(self):
        """Add a new medication entry."""
        self.medications_given.append(
            {"med": "", "dose": 0, "unit": ""}
        )

    @rx.event
    def update_medication(
        self, index: int, key: str, value: str | int
    ):
        """Update a specific medication entry."""
        if 0 <= index < len(self.medications_given):
            if key == "dose":
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    value = 0
            med_list = self.medications_given
            med_list[index][key] = value
            self.medications_given = med_list

    @rx.event
    def remove_medication(self, index: int):
        """Remove a medication entry."""
        if 0 <= index < len(self.medications_given):
            med_list = self.medications_given
            med_list.pop(index)
            self.medications_given = med_list

    @rx.event
    async def generate_narrative(self):
        """Generate narrative from EMS data."""
        print("Generating EMS narrative...")
        narrative = f"Unit {self.unit} dispatched for {self.dispatch_reason}. "
        narrative += f"Patient presented with {self.patient_presentation}. Chief complaint: {self.chief_complaint}. "
        if not self.vitals_wnl:
            narrative += f"Vitals: BP {self.bp_systolic}/{self.bp_diastolic}, HR {self.hr}, RR {self.rr}. "
        else:
            narrative += "Vitals WNL. "
        narrative += f"LOC: {self.level_of_consciousness}. "
        if self.interventions:
            narrative += f"Interventions: {', '.join(self.interventions)}. "
        if self.medications_given:
            narrative += f"Medications: {'; '.join([f'{m['med']} {m['dose']} {m['unit']}' for m in self.medications_given if m['med']])}. "
        narrative += f"Transported {self.transport_mode} to {self.destination_facility}."
        self.ems_narrative = narrative
        narrative_preview = narrative[:50] + "..."
        from app.states.session_state import SessionState

        session_state = await self.get_state(SessionState)
        await session_state.add_session(
            "EMS", narrative_preview
        )

    @rx.event
    def set_unit(self, value: str):
        self.unit = value

    @rx.event
    def set_dispatch_reason(self, value: str):
        self.dispatch_reason = value

    @rx.event
    def set_response_delay(self, value: str):
        self.response_delay = value

    @rx.event
    def set_patient_presentation(self, value: str):
        self.patient_presentation = value

    @rx.event
    def set_chief_complaint(self, value: str):
        self.chief_complaint = value

    @rx.event
    def set_opqrst_onset(self, value: str):
        self.opqrst_data["onset"] = value

    @rx.event
    def set_opqrst_provocation(self, value: str):
        self.opqrst_data["provocation"] = value

    @rx.event
    def set_opqrst_quality(self, value: str):
        self.opqrst_data["quality"] = value

    @rx.event
    def set_opqrst_radiation(self, value: str):
        self.opqrst_data["radiation"] = value

    @rx.event
    def set_opqrst_severity(self, value: str):
        self.opqrst_data["severity"] = value

    @rx.event
    def set_opqrst_time(self, value: str):
        self.opqrst_data["time"] = value

    @rx.event
    def set_vitals_wnl(self, value: bool):
        self.vitals_wnl = value

    @rx.event
    def set_bp_systolic(self, value: int):
        self.bp_systolic = value

    @rx.event
    def set_bp_diastolic(self, value: int):
        self.bp_diastolic = value

    @rx.event
    def set_hr(self, value: int):
        self.hr = value

    @rx.event
    def set_rr(self, value: int):
        self.rr = value

    @rx.event
    def set_level_of_consciousness(self, value: str):
        self.level_of_consciousness = value

    @rx.event
    def set_destination_facility(self, value: str):
        self.destination_facility = value

    @rx.event
    def set_transport_mode(self, value: str):
        self.transport_mode = value

    @rx.event
    def set_room_number(self, value: str):
        self.room_number = value

    @rx.event
    def set_receiving_staff(self, value: str):
        self.receiving_staff = value
import reflex as rx
from typing import Dict, List, Any, TypedDict
from app.states.session_state import SessionState


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
        "Trauma - Adult",
        "Trauma - Pediatric",
        "Allergic Reaction",
        "Seizure",
        "Overdose",
        "Respiratory Distress",
    ]
    interventions: List[str] = []
    all_interventions: List[str] = [
        "IV Establishment",
        "IO Access",
        "Oxygen Administration",
        "Medication Administration",
        "Airway Management (BVM)",
        "Intubation",
        "CPAP",
        "Defibrillation",
        "Cardioversion",
        "Pacing",
        "Splinting",
        "Bleeding Control",
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
        current_selection = set(self.protocol_selection)
        if checked:
            current_selection.add(protocol)
        else:
            current_selection.discard(protocol)
        self.protocol_selection = sorted(
            list(current_selection)
        )

    @rx.event
    def toggle_intervention(
        self, intervention: str, checked: bool
    ):
        """Add or remove an intervention from the list."""
        current_selection = set(self.interventions)
        if checked:
            current_selection.add(intervention)
        else:
            current_selection.discard(intervention)
        self.interventions = sorted(list(current_selection))

    @rx.event
    def add_medication(self):
        """Add a new medication entry."""
        new_list = self.medications_given + [
            {"med": "", "dose": "", "unit": ""}
        ]
        self.medications_given = new_list

    @rx.event
    def update_medication(
        self, index: int, key: str, value: str
    ):
        """Update a specific medication entry."""
        if 0 <= index < len(self.medications_given):
            med_list = list(self.medications_given)
            med_list[index] = med_list[index].copy()
            med_list[index][key] = value
            self.medications_given = med_list

    @rx.event
    def remove_medication(self, index: int):
        """Remove a medication entry."""
        if 0 <= index < len(self.medications_given):
            med_list = list(self.medications_given)
            med_list.pop(index)
            self.medications_given = med_list

    @rx.event
    async def generate_narrative(self):
        """Generate narrative from EMS data."""
        print("Generating EMS narrative...")
        narrative = f"Unit {self.unit or '[Unit]'}"
        narrative += f" dispatched for {self.dispatch_reason or '[Reason]'}. "
        if self.response_delay != "None":
            narrative += f"Response delay noted: {self.response_delay}. "
        narrative += f"On arrival, scene described as: {self.patient_presentation or '[Scene]'}. "
        narrative += f"Patient presents with chief complaint of {self.chief_complaint or '[Complaint]'}. "
        opqrst_parts = [
            f"{k.capitalize()}: {v}"
            for k, v in self.opqrst_data.items()
            if v
        ]
        if opqrst_parts:
            narrative += (
                f"OPQRST: {', '.join(opqrst_parts)}. "
            )
        if not self.vitals_wnl:
            vitals_str = f"BP {self.bp_systolic or 'N/A'}/{self.bp_diastolic or 'N/A'}, "
            vitals_str += f"HR {self.hr or 'N/A'}, RR {self.rr or 'N/A'}."
            narrative += f"Vitals: {vitals_str} "
        else:
            narrative += (
                "Vitals assessed as Within Normal Limits. "
            )
        narrative += f"Level of Consciousness: {self.level_of_consciousness or '[LOC]'}. "
        if self.protocol_selection:
            narrative += f"Protocols considered/followed: {', '.join(self.protocol_selection)}. "
        if self.interventions:
            narrative += f"Interventions performed: {', '.join(self.interventions)}. "
        if self.medications_given:
            med_strings = [
                f"{m['med']} {m['dose']}{m['unit']}"
                for m in self.medications_given
                if m["med"]
            ]
            if med_strings:
                narrative += f"Medications administered: {'; '.join(med_strings)}. "
        narrative += f"Patient transported via {self.transport_mode or '[Mode]'}"
        narrative += f" to {self.destination_facility or '[Facility]'}. "
        if self.room_number:
            narrative += (
                f"Patient left in {self.room_number}. "
            )
        if self.receiving_staff:
            narrative += f"Care transferred to {self.receiving_staff}. "
        async with self:
            self.ems_narrative = narrative.strip()
        yield rx.toast.success(
            "EMS narrative generated!",
            duration=2000,
            position="top-center",
        )
        narrative_preview = self.ems_narrative[:50] + (
            "..." if len(self.ems_narrative) > 50 else ""
        )
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
    def set_bp_systolic(self, value: str):
        self.bp_systolic = (
            int(value) if value.isdigit() else 0
        )

    @rx.event
    def set_bp_diastolic(self, value: str):
        self.bp_diastolic = (
            int(value) if value.isdigit() else 0
        )

    @rx.event
    def set_hr(self, value: str):
        self.hr = int(value) if value.isdigit() else 0

    @rx.event
    def set_rr(self, value: str):
        self.rr = int(value) if value.isdigit() else 0

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
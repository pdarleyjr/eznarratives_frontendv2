import reflex as rx
from app.states.ems_state import EmsState
from app.states.ui_state import UiState
from typing import List


def form_section_button(
    icon: str, label: str, target_section: str
) -> rx.Component:
    """Button to switch EMS form sections."""
    is_active = (
        EmsState.active_ems_section == target_section
    )
    base_class = "flex flex-col items-center justify-center p-3 gap-1 rounded-lg group w-full text-center transition-colors duration-150 ease-in-out min-h-[60px] focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-1 dark:focus:ring-offset-gray-800"
    active_class = (
        f"{base_class} bg-primary/10 dark:bg-primary/20"
    )
    inactive_class = f"{base_class} hover:bg-gray-100 dark:hover:bg-gray-700/50"
    icon_base = "size-5"
    icon_active = f"{icon_base} stroke-primary"
    icon_inactive = f"{icon_base} stroke-neutral dark:stroke-gray-400 group-hover:stroke-gray-600 dark:group-hover:stroke-gray-300 transition-colors"
    label_base = "text-xs sm:text-sm font-medium"
    label_active = f"{label_base} text-primary"
    label_inactive = f"{label_base} text-neutral dark:text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-300 transition-colors"
    return rx.el.button(
        rx.icon(
            tag=icon,
            class_name=rx.cond(
                is_active, icon_active, icon_inactive
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                is_active, label_active, label_inactive
            ),
        ),
        on_click=lambda: EmsState.set_active_ems_section(
            target_section
        ),
        class_name=rx.cond(
            is_active, active_class, inactive_class
        ),
        aria_label=f"Go to {label} section",
        type="button",
    )


def form_input(
    label: str, name: str, type: str = "text", **props
) -> rx.Component:
    """Reusable styled input field."""
    return rx.el.div(
        rx.el.label(
            label,
            html_for=name,
            class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5",
        ),
        rx.el.input(
            id=name,
            name=name,
            type=type,
            class_name="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:ring-2 focus:ring-primary focus:border-primary dark:focus:border-primary sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 transition-all duration-150 ease-in-out hover:border-gray-400 dark:hover:border-gray-500 min-h-[48px]",
            **props,
        ),
        class_name="mb-4",
    )


def form_textarea(
    label: str, name: str, **props
) -> rx.Component:
    """Reusable styled textarea."""
    rows_value = props.pop("rows", 3)
    return rx.el.div(
        rx.el.label(
            label,
            html_for=name,
            class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5",
        ),
        rx.el.textarea(
            id=name,
            name=name,
            rows=rows_value,
            class_name="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:ring-2 focus:ring-primary focus:border-primary dark:focus:border-primary sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 transition-all duration-150 ease-in-out hover:border-gray-400 dark:hover:border-gray-500 resize-y min-h-[80px]",
            **props,
        ),
        class_name="mb-4",
    )


def form_select(
    label: str,
    name: str,
    options: rx.Var[list[str]],
    **props,
) -> rx.Component:
    """Reusable styled select dropdown."""
    return rx.el.div(
        rx.el.label(
            label,
            html_for=name,
            class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5",
        ),
        rx.el.div(
            rx.el.select(
                rx.el.option(
                    f"Select {label}...",
                    value="",
                    disabled=True,
                    hidden=True,
                    class_name="text-gray-500",
                ),
                rx.foreach(
                    options,
                    lambda option: rx.el.option(
                        option, value=option
                    ),
                ),
                id=name,
                name=name,
                class_name="w-full appearance-none px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:ring-2 focus:ring-primary focus:border-primary dark:focus:border-primary sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white transition-all duration-150 ease-in-out hover:border-gray-400 dark:hover:border-gray-500 min-h-[48px] pr-10",
                **props,
            ),
            rx.icon(
                tag="chevron-down",
                size=20,
                class_name="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none stroke-gray-500 dark:stroke-gray-400",
            ),
            class_name="relative",
        ),
        class_name="mb-4",
    )


def form_checkbox(
    label: str, name: str, **props
) -> rx.Component:
    """Reusable styled checkbox."""
    return rx.el.div(
        rx.el.label(
            rx.el.input(
                type="checkbox",
                id=name,
                name=name,
                class_name="size-4 mr-2 rounded border-gray-300 dark:border-gray-600 text-primary focus:ring-2 focus:ring-primary focus:ring-offset-2 dark:focus:ring-offset-gray-800 bg-white dark:bg-gray-700 transition-colors cursor-pointer",
                **props,
            ),
            label,
            html_for=name,
            class_name="flex items-center text-sm font-medium text-gray-700 dark:text-gray-300 cursor-pointer",
        ),
        class_name="mb-4 min-h-[44px] flex items-center",
    )


def form_radio_group(
    label: str,
    name: str,
    options: rx.Var[list[str]],
    value: rx.Var[str],
    on_change: rx.event.EventHandler,
    **props,
) -> rx.Component:
    """Reusable styled radio button group."""
    return rx.el.fieldset(
        rx.el.legend(
            label,
            class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2",
        ),
        rx.el.div(
            rx.foreach(
                options,
                lambda option: rx.el.label(
                    rx.el.input(
                        type="radio",
                        name=name,
                        checked=value == option,
                        on_change=lambda _: on_change(
                            option
                        ),
                        class_name="size-4 mr-2 border-gray-300 dark:border-gray-600 text-primary focus:ring-2 focus:ring-primary focus:ring-offset-2 dark:focus:ring-offset-gray-800 bg-white dark:bg-gray-700 transition-colors cursor-pointer",
                        **props,
                    ),
                    option,
                    class_name="flex items-center mr-4 text-sm text-gray-700 dark:text-gray-300 cursor-pointer min-h-[44px]",
                    key=f"radio_{name}_{option}",
                ),
            ),
            class_name="flex flex-wrap gap-y-2 gap-x-4",
        ),
        class_name="mb-4",
    )


def dispatch_section() -> rx.Component:
    """Content for the Dispatch section."""
    return rx.el.div(
        form_input(
            "Unit",
            "unit",
            placeholder="e.g., Medic 1",
            default_value=EmsState.unit,
            key=f"{EmsState.active_ems_section}_unit",
            on_change=EmsState.set_unit,
        ),
        form_select(
            "Dispatch Reason",
            "dispatch_reason",
            EmsState.dispatch_reasons,
            value=EmsState.dispatch_reason,
            on_change=EmsState.set_dispatch_reason,
        ),
        form_select(
            "Response Delay",
            "response_delay",
            EmsState.response_delays,
            value=EmsState.response_delay,
            on_change=EmsState.set_response_delay,
        ),
        class_name="animate-fade-in",
    )


def arrival_section() -> rx.Component:
    """Content for the Arrival section."""
    return rx.el.div(
        form_textarea(
            "Patient Presentation / Scene Description",
            "patient_presentation",
            placeholder="Describe the scene and patient's initial appearance...",
            default_value=EmsState.patient_presentation,
            key=f"{EmsState.active_ems_section}_presentation",
            on_change=EmsState.set_patient_presentation,
        ),
        form_input(
            "Chief Complaint",
            "chief_complaint",
            placeholder="e.g., Chest Pain",
            default_value=EmsState.chief_complaint,
            key=f"{EmsState.active_ems_section}_complaint",
            on_change=EmsState.set_chief_complaint,
        ),
        rx.el.h4(
            "OPQRST",
            class_name="text-md font-semibold mb-3 text-gray-800 dark:text-gray-200",
        ),
        rx.el.div(
            form_input(
                "Onset",
                "onset",
                placeholder="When did it start?",
                default_value=EmsState.opqrst_data["onset"],
                key=f"{EmsState.active_ems_section}_onset",
                on_change=EmsState.set_opqrst_onset,
            ),
            form_input(
                "Provocation",
                "provocation",
                placeholder="What makes it better/worse?",
                default_value=EmsState.opqrst_data[
                    "provocation"
                ],
                key=f"{EmsState.active_ems_section}_provocation",
                on_change=EmsState.set_opqrst_provocation,
            ),
            form_input(
                "Quality",
                "quality",
                placeholder="Describe the pain/symptom",
                default_value=EmsState.opqrst_data[
                    "quality"
                ],
                key=f"{EmsState.active_ems_section}_quality",
                on_change=EmsState.set_opqrst_quality,
            ),
            form_input(
                "Radiation",
                "radiation",
                placeholder="Does it spread anywhere?",
                default_value=EmsState.opqrst_data[
                    "radiation"
                ],
                key=f"{EmsState.active_ems_section}_radiation",
                on_change=EmsState.set_opqrst_radiation,
            ),
            form_input(
                "Severity",
                "severity",
                type="number",
                placeholder="Scale 1-10",
                default_value=EmsState.opqrst_data[
                    "severity"
                ],
                key=f"{EmsState.active_ems_section}_severity",
                on_change=EmsState.set_opqrst_severity,
            ),
            form_input(
                "Time",
                "time",
                placeholder="Duration/Frequency",
                default_value=EmsState.opqrst_data["time"],
                key=f"{EmsState.active_ems_section}_time",
                on_change=EmsState.set_opqrst_time,
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-0",
        ),
        class_name="animate-fade-in",
    )


def assessment_section() -> rx.Component:
    """Content for the Assessment section."""
    return rx.el.div(
        form_checkbox(
            "Vitals Within Normal Limits (WNL)",
            "vitals_wnl",
            checked=EmsState.vitals_wnl,
            on_change=EmsState.set_vitals_wnl,
        ),
        rx.cond(
            ~EmsState.vitals_wnl,
            rx.el.div(
                form_input(
                    "BP Systolic",
                    "bp_systolic",
                    type="number",
                    default_value=EmsState.bp_systolic.to_string(),
                    key=f"bp_systolic_{EmsState.vitals_wnl.to_string()}",
                    on_change=EmsState.set_bp_systolic,
                ),
                form_input(
                    "BP Diastolic",
                    "bp_diastolic",
                    type="number",
                    default_value=EmsState.bp_diastolic.to_string(),
                    key=f"bp_diastolic_{EmsState.vitals_wnl.to_string()}",
                    on_change=EmsState.set_bp_diastolic,
                ),
                form_input(
                    "Heart Rate (HR)",
                    "hr",
                    type="number",
                    default_value=EmsState.hr.to_string(),
                    key=f"hr_{EmsState.vitals_wnl.to_string()}",
                    on_change=EmsState.set_hr,
                ),
                form_input(
                    "Respiratory Rate (RR)",
                    "rr",
                    type="number",
                    default_value=EmsState.rr.to_string(),
                    key=f"rr_{EmsState.vitals_wnl.to_string()}",
                    on_change=EmsState.set_rr,
                ),
                class_name="grid grid-cols-2 md:grid-cols-4 gap-x-4 gap-y-0",
            ),
            rx.fragment(),
        ),
        form_select(
            "Level of Consciousness (LOC)",
            "loc",
            EmsState.consciousness_levels,
            value=EmsState.level_of_consciousness,
            on_change=EmsState.set_level_of_consciousness,
        ),
        rx.el.div(
            rx.el.label(
                "Protocol Selection",
                class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    EmsState.protocols,
                    lambda protocol: form_checkbox(
                        protocol,
                        f"protocol_{protocol}",
                        checked=EmsState.protocol_selection.contains(
                            protocol
                        ),
                        on_change=lambda checked: EmsState.toggle_protocol(
                            protocol, checked
                        ),
                        key=f"protocol_cb_{protocol}",
                    ),
                ),
                class_name="space-y-1 max-h-40 overflow-y-auto border p-3 rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700/50 scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600",
            ),
            class_name="mb-4",
        ),
        class_name="animate-fade-in",
    )


def treatment_section() -> rx.Component:
    """Content for the Treatment section."""
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Interventions Performed",
                class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2",
            ),
            rx.el.div(
                rx.foreach(
                    EmsState.all_interventions,
                    lambda intervention: form_checkbox(
                        intervention,
                        f"intervention_{intervention}",
                        checked=EmsState.interventions.contains(
                            intervention
                        ),
                        on_change=lambda checked: EmsState.toggle_intervention(
                            intervention, checked
                        ),
                        key=f"intervention_cb_{intervention}",
                    ),
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-0",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Medications Given",
                    class_name="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2",
                ),
                rx.el.button(
                    rx.icon(
                        "plus",
                        size=14,
                        class_name="mr-1 stroke-current",
                    ),
                    "Add Med",
                    on_click=EmsState.add_medication,
                    class_name="text-xs bg-secondary dark:bg-gray-600 text-neutral dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-500 px-3 py-1.5 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-1 dark:focus:ring-offset-gray-800 transition-colors transform active:scale-95",
                    type="button",
                ),
                class_name="flex justify-between items-center mb-2",
            ),
            rx.el.div(
                rx.cond(
                    EmsState.medications_given.length()
                    == 0,
                    rx.el.p(
                        "No medications added yet.",
                        class_name="text-sm text-gray-500 dark:text-gray-400 italic",
                    ),
                    rx.foreach(
                        EmsState.medications_given,
                        lambda med, index: rx.el.div(
                            form_input(
                                "Medication",
                                f"med_name_{index}",
                                placeholder="e.g., Aspirin",
                                default_value=med["med"],
                                key=f"med_name_{index}_{EmsState.medications_given.length()}",
                                on_change=lambda v: EmsState.update_medication(
                                    index, "med", v
                                ),
                            ),
                            form_input(
                                "Dose",
                                f"med_dose_{index}",
                                type="text",
                                placeholder="e.g., 324 / neb",
                                default_value=med[
                                    "dose"
                                ].to_string(),
                                key=f"med_dose_{index}_{EmsState.medications_given.length()}",
                                on_change=lambda v: EmsState.update_medication(
                                    index, "dose", v
                                ),
                            ),
                            form_input(
                                "Unit",
                                f"med_unit_{index}",
                                placeholder="e.g., mg / ml",
                                default_value=med["unit"],
                                key=f"med_unit_{index}_{EmsState.medications_given.length()}",
                                on_change=lambda v: EmsState.update_medication(
                                    index, "unit", v
                                ),
                            ),
                            rx.el.button(
                                rx.icon(
                                    "trash-2",
                                    size=16,
                                    class_name="stroke-current",
                                ),
                                on_click=lambda: EmsState.remove_medication(
                                    index
                                ),
                                class_name="text-red-600 hover:text-red-700 dark:text-red-500 dark:hover:text-red-400 p-2 rounded-md hover:bg-red-100 dark:hover:bg-red-900/50 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-1 dark:focus:ring-offset-gray-800 transition-colors mt-5 transform active:scale-95",
                                type="button",
                                aria_label="Remove medication",
                            ),
                            class_name="grid grid-cols-[minmax(100px,_2fr)_minmax(60px,_1fr)_minmax(60px,_1fr)_auto] gap-x-2 items-end mb-2",
                            key=f"med_row_{index}",
                        ),
                    ),
                ),
                class_name="space-y-2",
            ),
            class_name="mb-4",
        ),
        class_name="animate-fade-in",
    )


def transport_section() -> rx.Component:
    """Content for the Transport section."""
    return rx.el.div(
        form_input(
            "Destination Facility",
            "destination_facility",
            placeholder="e.g., General Hospital",
            default_value=EmsState.destination_facility,
            key=f"{EmsState.active_ems_section}_destination",
            on_change=EmsState.set_destination_facility,
        ),
        form_radio_group(
            "Transport Mode",
            "transport_mode",
            options=EmsState.transport_modes,
            value=EmsState.transport_mode,
            on_change=EmsState.set_transport_mode,
        ),
        form_input(
            "Room Pt Left In",
            "room_number",
            placeholder="e.g., Room 3B / Bed 5",
            default_value=EmsState.room_number,
            key=f"{EmsState.active_ems_section}_room",
            on_change=EmsState.set_room_number,
        ),
        form_input(
            "Receiving RN/Dr",
            "receiving_staff",
            placeholder="Name of staff",
            default_value=EmsState.receiving_staff,
            key=f"{EmsState.active_ems_section}_staff",
            on_change=EmsState.set_receiving_staff,
        ),
        class_name="animate-fade-in",
    )


def ems_form() -> rx.Component:
    """EMS report form component."""
    return rx.el.div(
        rx.el.div(
            rx.cond(
                EmsState.ems_narrative,
                rx.el.p(
                    EmsState.ems_narrative,
                    class_name="text-sm text-gray-700 dark:text-gray-300 p-4 whitespace-pre-wrap",
                ),
                rx.el.p(
                    "Generated narrative will appear here...",
                    class_name="text-sm text-gray-500 dark:text-gray-400 italic p-4 text-center",
                ),
            ),
            class_name="h-[max(200px,30vh)] bg-gray-100 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent",
        ),
        rx.el.div(
            rx.el.div(
                form_section_button(
                    "siren", "Dispatch", "Dispatch"
                ),
                form_section_button(
                    "map-pin", "Arrival", "Arrival"
                ),
                form_section_button(
                    "clipboard-list",
                    "Assessment",
                    "Assessment",
                ),
                form_section_button(
                    "syringe", "Treatment", "Treatment"
                ),
                form_section_button(
                    "truck", "Transport", "Transport"
                ),
                class_name="grid grid-cols-5 gap-1 p-1 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 sticky top-0 z-10",
            ),
            rx.el.div(
                rx.el.div(
                    rx.match(
                        EmsState.active_ems_section,
                        ("Dispatch", dispatch_section()),
                        ("Arrival", arrival_section()),
                        (
                            "Assessment",
                            assessment_section(),
                        ),
                        ("Treatment", treatment_section()),
                        ("Transport", transport_section()),
                        rx.el.p("Select a section"),
                    ),
                    class_name="p-4 md:p-6 pb-20",
                    key=EmsState.active_ems_section,
                ),
                class_name="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-200 dark:scrollbar-thumb-gray-700 scrollbar-track-transparent",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "arrow-up",
                        class_name="stroke-current",
                        size=24,
                    ),
                    on_click=EmsState.generate_narrative,
                    class_name="w-11 h-11 p-2 rounded-lg text-white bg-accent hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 dark:focus:ring-offset-gray-900 shadow-lg transition-transform transform hover:scale-105 active:scale-95 flex items-center justify-center",
                    type="button",
                    aria_label="Generate EMS Narrative",
                ),
                class_name="absolute bottom-4 right-4 z-20",
            ),
            class_name="flex-1 flex flex-col overflow-hidden relative",
        ),
        class_name="flex flex-col h-full",
    )
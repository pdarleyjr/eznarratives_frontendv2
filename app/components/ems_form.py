import reflex as rx
from app.states.ems_state import EmsState


def ems_section_nav_item(
    icon: str, title: str, section_key: str
) -> rx.Component:
    """Navigation item for an EMS section."""
    is_active = EmsState.active_ems_section == section_key
    return rx.el.button(
        rx.icon(
            icon,
            size=20,
            class_name=rx.cond(
                is_active,
                "text-primary",
                "text-neutral group-hover:text-primary transition-colors",
            ),
        ),
        rx.el.span(
            title,
            class_name=rx.cond(
                is_active,
                "text-xs sm:text-sm font-medium text-primary mt-1 whitespace-nowrap",
                "text-xs sm:text-sm font-medium text-neutral group-hover:text-primary transition-colors mt-1 whitespace-nowrap",
            ),
        ),
        on_click=lambda: EmsState.set_active_ems_section(
            section_key
        ),
        class_name=rx.cond(
            is_active,
            "flex flex-col items-center p-2 sm:p-3 rounded-lg bg-blue-50 group border-b-2 border-primary transition-all duration-150 ease-in-out min-h-[56px] min-w-[56px] justify-center",
            "flex flex-col items-center p-2 sm:p-3 rounded-lg hover:bg-secondary group border-b-2 border-transparent transition-all duration-150 ease-in-out min-h-[56px] min-w-[56px] justify-center",
        ),
        type="button",
        aria_label=f"Go to {title} section",
    )


def form_input(
    label: str,
    state_setter,
    default_value,
    input_type="text",
    **kwargs,
) -> rx.Component:
    """Reusable styled input component."""
    outer_class_name = kwargs.pop("class_name", "")
    input_class_name = "mt-1 block w-full rounded-md border border-gray-300 bg-white shadow-sm focus:border-primary focus:ring focus:ring-blue-200 focus:ring-opacity-50 text-sm px-4 py-2.5 transition-shadow h-11"
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-xs font-medium text-neutral mb-1",
        ),
        rx.el.input(
            type=input_type,
            on_change=state_setter,
            default_value=default_value,
            class_name=input_class_name,
            **kwargs,
        ),
        class_name=outer_class_name,
    )


def form_select(
    label: str, options, state_var, state_setter, **kwargs
) -> rx.Component:
    """Reusable styled select component."""
    outer_class_name = kwargs.pop("class_name", "")
    select_class_name = "mt-1 block w-full rounded-md border border-gray-300 bg-white shadow-sm focus:border-primary focus:ring focus:ring-blue-200 focus:ring-opacity-50 text-sm px-4 py-2.5 transition-shadow h-11 appearance-none pr-8 bg-no-repeat bg-right-2"
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-xs font-medium text-neutral mb-1",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    options,
                    lambda option: rx.el.option(
                        option, value=option
                    ),
                ),
                value=state_var,
                on_change=state_setter,
                class_name=select_class_name,
                style={
                    "backgroundImage": 'url(\'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20"%3E%3Cpath stroke="%236B7280" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 8l4 4 4-4"/%3E%3C/svg%3E\')'
                },
                **kwargs,
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none",
            ),
            class_name="relative mt-1",
        ),
        class_name=outer_class_name,
    )


def form_textarea(
    label: str,
    state_setter,
    default_value,
    rows=4,
    **kwargs,
) -> rx.Component:
    """Reusable styled textarea component."""
    outer_class_name = kwargs.pop("class_name", "")
    textarea_class_name = "mt-1 block w-full rounded-md border border-gray-300 bg-white shadow-sm focus:border-primary focus:ring focus:ring-blue-200 focus:ring-opacity-50 text-sm px-4 py-2.5 transition-shadow"
    return rx.el.div(
        rx.el.label(
            label,
            class_name="block text-xs font-medium text-neutral mb-1",
        ),
        rx.el.textarea(
            on_change=state_setter,
            default_value=default_value,
            rows=rows,
            class_name=textarea_class_name,
            **kwargs,
        ),
        class_name=outer_class_name,
    )


def ems_section_content(section_key: str) -> rx.Component:
    """Renders the content for the active EMS section with responsive grid."""
    base_grid = "grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-4 p-4 sm:p-6"
    wide_grid = "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-x-6 gap-y-4 p-4 sm:p-6"
    treatment_grid = "p-4 sm:p-6 space-y-6"
    return rx.match(
        section_key,
        (
            "Dispatch",
            rx.el.div(
                form_input(
                    "Unit",
                    EmsState.set_unit,
                    EmsState.unit,
                    class_name="col-span-1",
                ),
                form_select(
                    "Dispatch Reason",
                    EmsState.dispatch_reasons,
                    EmsState.dispatch_reason,
                    EmsState.set_dispatch_reason,
                    class_name="col-span-1",
                ),
                form_select(
                    "Response Delay",
                    EmsState.response_delays,
                    EmsState.response_delay,
                    EmsState.set_response_delay,
                    class_name="col-span-1",
                ),
                class_name=base_grid,
            ),
        ),
        (
            "Arrival",
            rx.el.div(
                form_textarea(
                    "Patient Presentation",
                    EmsState.set_patient_presentation,
                    EmsState.patient_presentation,
                    rows=3,
                    class_name="col-span-full",
                ),
                form_input(
                    "Chief Complaint",
                    EmsState.set_chief_complaint,
                    EmsState.chief_complaint,
                    class_name="col-span-full",
                ),
                rx.el.h4(
                    "OPQRST",
                    class_name="col-span-full text-sm font-semibold text-neutral mt-4 mb-2 border-t pt-4",
                ),
                form_input(
                    "Onset",
                    EmsState.set_opqrst_onset,
                    EmsState.opqrst_data["onset"],
                    class_name="col-span-1",
                ),
                form_input(
                    "Provocation/Palliation",
                    EmsState.set_opqrst_provocation,
                    EmsState.opqrst_data["provocation"],
                    class_name="col-span-1",
                ),
                form_input(
                    "Quality",
                    EmsState.set_opqrst_quality,
                    EmsState.opqrst_data["quality"],
                    class_name="col-span-1",
                ),
                form_input(
                    "Radiation",
                    EmsState.set_opqrst_radiation,
                    EmsState.opqrst_data["radiation"],
                    class_name="col-span-1",
                ),
                form_input(
                    "Severity (1-10)",
                    EmsState.set_opqrst_severity,
                    EmsState.opqrst_data["severity"],
                    class_name="col-span-1",
                ),
                form_input(
                    "Time",
                    EmsState.set_opqrst_time,
                    EmsState.opqrst_data["time"],
                    class_name="col-span-1",
                ),
                class_name=base_grid
                + " sm:grid-cols-2 md:grid-cols-3",
            ),
        ),
        (
            "Assessment",
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        rx.el.input(
                            type="checkbox",
                            checked=EmsState.vitals_wnl,
                            on_change=EmsState.set_vitals_wnl,
                            class_name="mr-2 rounded border-gray-400 text-primary shadow-sm focus:ring-primary h-5 w-5",
                        ),
                        "Vitals WNL",
                        class_name="inline-flex items-center text-sm font-medium text-neutral cursor-pointer p-2",
                    ),
                    class_name="col-span-full mb-4",
                ),
                form_input(
                    "BP Systolic",
                    lambda v: EmsState.set_bp_systolic(
                        rx.cond(v, v.to(int), 0)
                    ),
                    EmsState.bp_systolic.to_string(),
                    input_type="number",
                    disabled=EmsState.vitals_wnl,
                    class_name="col-span-1",
                ),
                form_input(
                    "BP Diastolic",
                    lambda v: EmsState.set_bp_diastolic(
                        rx.cond(v, v.to(int), 0)
                    ),
                    EmsState.bp_diastolic.to_string(),
                    input_type="number",
                    disabled=EmsState.vitals_wnl,
                    class_name="col-span-1",
                ),
                form_input(
                    "Heart Rate",
                    lambda v: EmsState.set_hr(
                        rx.cond(v, v.to(int), 0)
                    ),
                    EmsState.hr.to_string(),
                    input_type="number",
                    disabled=EmsState.vitals_wnl,
                    class_name="col-span-1",
                ),
                form_input(
                    "Respirations",
                    lambda v: EmsState.set_rr(
                        rx.cond(v, v.to(int), 0)
                    ),
                    EmsState.rr.to_string(),
                    input_type="number",
                    disabled=EmsState.vitals_wnl,
                    class_name="col-span-1",
                ),
                form_select(
                    "Level of Consciousness",
                    EmsState.consciousness_levels,
                    EmsState.level_of_consciousness,
                    EmsState.set_level_of_consciousness,
                    class_name="col-span-full sm:col-span-2",
                ),
                class_name=wide_grid,
            ),
        ),
        (
            "Treatment",
            rx.el.div(
                rx.el.fieldset(
                    rx.el.legend(
                        "Protocols Selected",
                        class_name="block text-xs font-semibold text-neutral mb-2 uppercase tracking-wider",
                    ),
                    rx.el.div(
                        rx.foreach(
                            EmsState.protocols,
                            lambda protocol: rx.el.label(
                                rx.el.input(
                                    type="checkbox",
                                    checked=EmsState.protocol_selection.contains(
                                        protocol
                                    ),
                                    on_change=lambda checked: EmsState.toggle_protocol(
                                        protocol, checked
                                    ),
                                    class_name="mr-2 rounded border-gray-400 text-primary shadow-sm focus:ring-primary h-5 w-5",
                                ),
                                protocol,
                                class_name="inline-flex items-center mr-4 mb-2 text-sm text-neutral cursor-pointer p-1",
                            ),
                        ),
                        class_name="flex flex-wrap gap-x-4 gap-y-2",
                    ),
                ),
                rx.el.fieldset(
                    rx.el.legend(
                        "Interventions Performed",
                        class_name="block text-xs font-semibold text-neutral mb-2 uppercase tracking-wider border-t pt-4 mt-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            EmsState.all_interventions,
                            lambda intervention: rx.el.label(
                                rx.el.input(
                                    type="checkbox",
                                    checked=EmsState.interventions.contains(
                                        intervention
                                    ),
                                    on_change=lambda checked: EmsState.toggle_intervention(
                                        intervention,
                                        checked,
                                    ),
                                    class_name="mr-2 rounded border-gray-400 text-primary shadow-sm focus:ring-primary h-5 w-5",
                                ),
                                intervention,
                                class_name="inline-flex items-center mr-4 mb-2 text-sm text-neutral cursor-pointer p-1",
                            ),
                        ),
                        class_name="flex flex-wrap gap-x-4 gap-y-2",
                    ),
                ),
                rx.el.fieldset(
                    rx.el.legend(
                        "Medications Given",
                        class_name="block text-xs font-semibold text-neutral mb-2 uppercase tracking-wider border-t pt-4 mt-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            EmsState.medications_given,
                            lambda med_entry, index: rx.el.div(
                                form_input(
                                    "",
                                    lambda v: EmsState.update_medication(
                                        index, "med", v
                                    ),
                                    med_entry["med"],
                                    placeholder="Medication Name",
                                    aria_label="Medication Name",
                                    class_name="flex-1 min-w-[150px]",
                                ),
                                form_input(
                                    "",
                                    lambda v: EmsState.update_medication(
                                        index,
                                        "dose",
                                        rx.cond(
                                            v, v.to(int), 0
                                        ),
                                    ),
                                    med_entry[
                                        "dose"
                                    ].to_string(),
                                    input_type="number",
                                    placeholder="Dose",
                                    aria_label="Dose",
                                    class_name="w-24",
                                ),
                                form_input(
                                    "",
                                    lambda v: EmsState.update_medication(
                                        index, "unit", v
                                    ),
                                    med_entry["unit"],
                                    placeholder="Unit",
                                    aria_label="Unit",
                                    class_name="w-20",
                                ),
                                rx.el.button(
                                    rx.icon(
                                        "trash", size=18
                                    ),
                                    on_click=lambda: EmsState.remove_medication(
                                        index
                                    ),
                                    type="button",
                                    aria_label="Remove Medication",
                                    class_name="p-2.5 rounded-md text-red-600 hover:bg-red-100 transition-colors flex-shrink-0 self-end mb-1 h-11 w-11 flex items-center justify-center",
                                ),
                                class_name="flex flex-wrap gap-3 mb-3 items-start",
                            ),
                        )
                    ),
                    rx.el.button(
                        rx.icon("plus", size=18),
                        "Add Medication",
                        on_click=EmsState.add_medication,
                        type="button",
                        class_name="inline-flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-neutral bg-white hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary",
                    ),
                ),
                class_name=treatment_grid,
            ),
        ),
        (
            "Transport",
            rx.el.div(
                form_input(
                    "Destination Facility",
                    EmsState.set_destination_facility,
                    EmsState.destination_facility,
                    class_name="col-span-full sm:col-span-1",
                ),
                form_select(
                    "Transport Mode",
                    EmsState.transport_modes,
                    EmsState.transport_mode,
                    EmsState.set_transport_mode,
                    class_name="col-span-1",
                ),
                form_input(
                    "Room Number",
                    EmsState.set_room_number,
                    EmsState.room_number,
                    class_name="col-span-1",
                ),
                form_input(
                    "Receiving Staff (RN/Dr)",
                    EmsState.set_receiving_staff,
                    EmsState.receiving_staff,
                    class_name="col-span-full sm:col-span-1",
                ),
                class_name=base_grid + " md:grid-cols-3",
            ),
        ),
        rx.el.div(
            "Select a section",
            class_name="p-6 text-neutral text-center",
        ),
    )


def ems_form() -> rx.Component:
    """Container for the EMS report form, including response window and sectioned inputs."""
    return rx.el.div(
        rx.scroll_area(
            rx.el.div(
                rx.cond(
                    EmsState.ems_narrative,
                    rx.el.pre(
                        EmsState.ems_narrative,
                        class_name="text-sm text-gray-800 whitespace-pre-wrap font-sans leading-relaxed",
                    ),
                    rx.el.p(
                        "Generated narrative will appear here.",
                        class_name="text-sm text-gray-500 italic",
                    ),
                ),
                class_name="p-4 sm:p-6",
            ),
            scrollbars="vertical",
            type="auto",
            class_name="flex-shrink-0 h-[25vh] md:h-[30vh] border border-gray-200 rounded-t-lg bg-white mb-0 shadow-sm overflow-y-auto",
        ),
        rx.el.div(
            rx.el.div(
                ems_section_nav_item(
                    "siren", "Dispatch", "Dispatch"
                ),
                ems_section_nav_item(
                    "heart-pulse", "Arrival", "Arrival"
                ),
                ems_section_nav_item(
                    "stethoscope",
                    "Assessment",
                    "Assessment",
                ),
                ems_section_nav_item(
                    "syringe", "Treatment", "Treatment"
                ),
                ems_section_nav_item(
                    "ambulance", "Transport", "Transport"
                ),
                class_name="grid grid-cols-5 gap-1 sm:gap-2 border-y border-gray-200 bg-gray-50 p-1 sm:p-2 sticky top-0 z-10",
            ),
            rx.scroll_area(
                ems_section_content(
                    EmsState.active_ems_section
                ),
                scrollbars="vertical",
                type="auto",
                class_name="flex-grow bg-white",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("arrow_up", size=24),
                    type="button",
                    on_click=EmsState.generate_narrative,
                    class_name="p-3 rounded-full text-white bg-primary hover:bg-accent focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-colors duration-150 ease-in-out h-12 w-12 flex items-center justify-center shadow-lg",
                    aria_label="Generate EMS Narrative",
                ),
                class_name="p-4 border-t border-gray-200 bg-gray-50 flex-shrink-0 flex justify-end items-center",
            ),
            class_name="flex-grow flex flex-col border border-gray-200 rounded-b-lg shadow-sm overflow-hidden bg-white",
        ),
        class_name="p-4 sm:p-6 flex flex-col h-full bg-gray-100 pb-[calc(env(safe-area-inset-bottom)+1rem)]",
    )
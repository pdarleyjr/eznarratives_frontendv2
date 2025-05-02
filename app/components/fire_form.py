import reflex as rx
from app.states.fire_state import FireState
from app.states.ui_state import UiState
from app.components.ems_form import (
    form_input,
    form_select,
    form_textarea,
)


def fire_form() -> rx.Component:
    """Fire report form component."""
    return rx.el.div(
        rx.el.div(
            rx.cond(
                FireState.fire_narrative,
                rx.el.p(
                    FireState.fire_narrative,
                    class_name="text-sm text-gray-700 dark:text-gray-300 p-4 whitespace-pre-wrap",
                ),
                rx.el.p(
                    "Generated narrative will appear here...",
                    class_name="text-sm text-gray-500 dark:text-gray-400 italic p-4 text-center",
                ),
            ),
            class_name="h-[calc(50%-2rem)] md:h-[calc(50%-4rem)] bg-gray-100 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent",
        ),
        rx.el.div(
            rx.el.div(
                form_input(
                    "Unit",
                    "fire_unit",
                    placeholder="e.g., Engine 1",
                    default_value=FireState.unit,
                    on_change=FireState.set_unit,
                    key=f"fire_unit_{FireState.unit}",
                ),
                form_select(
                    "Emergency Type",
                    "emergency_type",
                    FireState.emergency_types,
                    value=FireState.emergency_type,
                    on_change=FireState.set_emergency_type,
                ),
                form_textarea(
                    "Additional Information",
                    "additional_information",
                    placeholder="Provide any other relevant details...",
                    default_value=FireState.additional_information,
                    on_change=FireState.set_additional_information,
                    key=f"fire_info_{FireState.additional_information}",
                    rows=5,
                ),
                class_name="p-4 md:p-6 flex-grow pb-20",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "arrow-up",
                        class_name="stroke-current",
                        size=24,
                    ),
                    on_click=FireState.generate_narrative,
                    class_name="w-11 h-11 p-2 rounded-lg text-white bg-accent hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-accent focus:ring-offset-2 dark:focus:ring-offset-gray-900 shadow-md transition-transform transform hover:scale-105 active:scale-95 flex items-center justify-center",
                    type="button",
                    aria_label="Generate Fire Narrative",
                ),
                class_name="absolute bottom-4 right-4 z-10",
            ),
            class_name="flex-1 overflow-y-auto flex flex-col relative",
        ),
        class_name="flex flex-col h-full",
    )
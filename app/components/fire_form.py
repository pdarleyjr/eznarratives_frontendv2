import reflex as rx
from app.states.fire_state import FireState
from app.components.ems_form import (
    form_input,
    form_select,
    form_textarea,
)


def fire_form() -> rx.Component:
    """Container for the Fire report form, including response window and inputs."""
    return rx.el.div(
        rx.scroll_area(
            rx.el.div(
                rx.cond(
                    FireState.fire_narrative,
                    rx.el.pre(
                        FireState.fire_narrative,
                        class_name="text-sm sm:text-base text-gray-800 whitespace-pre-wrap font-sans leading-relaxed",
                    ),
                    rx.el.p(
                        "Generated narrative will appear here.",
                        class_name="text-sm sm:text-base text-gray-500 italic",
                    ),
                ),
                class_name="p-4 sm:p-6",
            ),
            scrollbars="vertical",
            type="auto",
            class_name="flex-shrink-0 h-[25vh] md:h-[30vh] border border-gray-200 rounded-lg bg-white mb-4 shadow-sm overflow-y-auto",
        ),
        rx.el.div(
            rx.scroll_area(
                rx.el.div(
                    form_input(
                        "Unit",
                        FireState.set_unit,
                        FireState.unit,
                        class_name="mb-4",
                    ),
                    form_select(
                        "Emergency Type",
                        FireState.emergency_types,
                        FireState.emergency_type,
                        FireState.set_emergency_type,
                        class_name="mb-4",
                    ),
                    form_textarea(
                        "Additional Information",
                        FireState.set_additional_information,
                        FireState.additional_information,
                        rows=8,
                        class_name="mb-4 flex-grow",
                    ),
                    class_name="p-4 sm:p-6 flex flex-col h-full",
                ),
                scrollbars="vertical",
                type="auto",
                class_name="flex-grow bg-white",
            ),
            rx.el.div(
                rx.el.button(
                    "Generate Fire Narrative",
                    type="button",
                    on_click=FireState.generate_narrative,
                    class_name="w-full px-6 py-4 border border-transparent rounded-md shadow-sm text-lg font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-150 ease-in-out min-h-[50px]",
                ),
                class_name="p-4 border-t border-gray-200 bg-gray-50 flex-shrink-0 pb-[calc(env(safe-area-inset-bottom)+1rem)]",
            ),
            class_name="flex-grow flex flex-col border border-gray-200 rounded-lg shadow-sm overflow-hidden bg-white",
        ),
        class_name="p-4 sm:p-6 flex flex-col h-full bg-gray-100",
    )
import reflex as rx
from app.states.ui_state import UiState


def header() -> rx.Component:
    """Renders the application header."""
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon(
                    tag="menu",
                    size=24,
                    class_name="text-gray-600 dark:text-gray-300",
                ),
                on_click=UiState.toggle_sidebar,
                class_name="p-2 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary transition-colors transform active:scale-95",
                aria_label="Toggle sidebar",
            ),
            rx.el.div(
                rx.icon(
                    tag="box",
                    size=28,
                    class_name="text-primary mr-2 flex-shrink-0",
                ),
                rx.el.span(
                    "EZ Narratives",
                    class_name="text-xl font-semibold text-gray-800 dark:text-white whitespace-nowrap",
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                rx.icon(
                    tag=rx.cond(
                        UiState.theme_appearance == "light",
                        "moon",
                        "sun",
                    ),
                    size=20,
                ),
                on_click=UiState.toggle_theme,
                class_name="p-2 rounded-md text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary transition-colors transform active:scale-95",
                aria_label="Toggle theme",
            ),
            class_name="flex items-center justify-between w-full h-16 px-4 border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-neutral-800/80 backdrop-blur-md shadow-sm",
        ),
        class_name="fixed top-0 left-0 right-0 z-30 w-full pt-safe-top",
    )
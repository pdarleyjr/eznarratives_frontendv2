import reflex as rx
from app.states.ui_state import UiState
from app.states.chat_state import ChatState
from app.components.ems_form import ems_form
from app.components.fire_form import fire_form
from app.components.input_area import input_area
from app.components.preset_cards import preset_cards
from app.components.message_bubble import message_bubble


def chat_content() -> rx.Component:
    """Content for the Chat tab."""
    return rx.el.div(
        rx.el.div(
            rx.cond(
                ChatState.messages,
                rx.scroll_area(
                    rx.el.div(
                        rx.foreach(
                            ChatState.messages,
                            lambda m, i: message_bubble(
                                m["text"],
                                m["is_ai"],
                                i
                                == ChatState.messages.length()
                                - 1,
                            ),
                        ),
                        class_name="flex flex-col gap-8 p-4 sm:p-6 lg:p-8 pb-10",
                    ),
                    scrollbars="vertical",
                    type="auto",
                    class_name="flex-grow",
                ),
                preset_cards(),
            ),
            class_name="flex-grow overflow-hidden relative flex flex-col",
        ),
        rx.el.div(
            input_area(),
            class_name="p-4 bg-gray-50 border-t border-gray-200 sticky bottom-0 pb-[calc(env(safe-area-inset-bottom)+1rem)]",
        ),
        class_name="flex flex-col h-full bg-gray-50",
    )


def tab_button(tab_name: str) -> rx.Component:
    """A single tab button."""
    return rx.el.button(
        tab_name,
        on_click=lambda: UiState.set_active_tab(tab_name),
        class_name=rx.cond(
            UiState.active_tab == tab_name,
            "px-4 py-2 border-b-2 border-blue-600 text-blue-600 font-medium text-sm sm:text-base transition-colors duration-150 ease-in-out min-h-[44px] flex items-center",
            "px-4 py-2 border-b-2 border-transparent text-gray-600 hover:text-blue-600 hover:border-blue-600 text-sm sm:text-base transition-colors duration-150 ease-in-out min-h-[44px] flex items-center",
        ),
        type="button",
    )


def app_header() -> rx.Component:
    """Header containing menu toggle for mobile."""
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon(
                    rx.cond(
                        UiState.sidebar_open, "x", "menu"
                    ),
                    size=24,
                ),
                on_click=UiState.toggle_sidebar,
                class_name="p-2 text-gray-600 hover:bg-gray-100 rounded-md lg:hidden h-11 w-11 flex items-center justify-center",
                type="button",
                aria_label="Toggle Menu",
            ),
            rx.el.div(class_name="flex-1"),
        ),
        class_name="sticky top-0 z-20 bg-white border-b border-gray-200 h-16 flex items-center px-4 pt-[env(safe-area-inset-top)]",
    )


def tab_bar() -> rx.Component:
    """Tab bar component."""
    return rx.el.div(
        tab_button("Chat"),
        tab_button("EMS"),
        tab_button("Fire"),
        class_name="flex border-b border-gray-200 bg-white z-10 items-center px-4 h-14 justify-around sm:justify-start",
    )


def tab_container() -> rx.Component:
    """Container for the header, tab bar, and tab content."""
    return rx.el.div(
        app_header(),
        tab_bar(),
        rx.el.div(
            rx.match(
                UiState.active_tab,
                ("Chat", chat_content()),
                ("EMS", ems_form()),
                ("Fire", fire_form()),
                rx.el.div("Select a tab", class_name="p-6"),
            ),
            class_name="flex-grow overflow-hidden",
        ),
        class_name="flex flex-col h-full",
    )
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
                        class_name="flex flex-col gap-6 p-4 sm:p-6 lg:p-8 pb-24",
                    ),
                    scrollbars="vertical",
                    type="auto",
                    class_name="absolute inset-0 overflow-y-auto",
                ),
                preset_cards(),
            ),
            class_name="flex-grow overflow-hidden relative flex flex-col",
        ),
        rx.el.div(
            input_area(),
            class_name="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-gray-100 via-gray-100 to-transparent z-10 pb-[calc(env(safe-area-inset-bottom)+1rem)]",
        ),
        class_name="flex flex-col h-full bg-background relative",
    )


def tab_button(
    tab_name: str, icon_name: str
) -> rx.Component:
    """A single tab button with icon and text."""
    is_active = UiState.active_tab == tab_name
    return rx.el.button(
        rx.icon(
            icon_name,
            size=20,
            class_name=rx.cond(
                is_active,
                "text-primary",
                "text-neutral group-hover:text-primary transition-colors",
            ),
        ),
        rx.el.span(tab_name, class_name="ml-2"),
        on_click=lambda: UiState.set_active_tab(tab_name),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 border-b-2 border-primary text-primary font-medium text-sm sm:text-base transition-colors duration-150 ease-in-out min-h-[48px] flex items-center justify-center group",
            "px-4 py-2 border-b-2 border-transparent text-neutral hover:text-primary hover:border-gray-300 text-sm sm:text-base transition-colors duration-150 ease-in-out min-h-[48px] flex items-center justify-center group",
        ),
        type="button",
        aria_selected=rx.cond(is_active, "true", "false"),
        role="tab",
        aria_label=f"Select {tab_name} tab",
    )


def app_header() -> rx.Component:
    """Header containing menu toggle, logo, and app title."""
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", size=24),
                on_click=UiState.toggle_sidebar,
                class_name="p-2 text-neutral hover:bg-secondary rounded-md lg:hidden h-11 w-11 flex items-center justify-center",
                type="button",
                aria_label="Open Menu",
                aria_controls="main-sidebar",
                aria_expanded=UiState.sidebar_open,
            ),
            rx.el.div(
                rx.el.img(
                    src="/favicon.ico",
                    alt="EZ Narratives Logo",
                    class_name="h-7 w-7 mr-2",
                ),
                rx.el.h1(
                    "EZ Narratives",
                    class_name="text-lg font-semibold text-gray-800 whitespace-nowrap",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(class_name="flex-1"),
            rx.el.div(class_name="w-11 lg:hidden"),
        ),
        class_name="sticky top-0 z-30 bg-white border-b border-gray-200 h-16 flex items-center px-4 pt-[env(safe-area-inset-top)] shadow-sm",
    )


def tab_bar() -> rx.Component:
    """Tab bar component placed below the header."""
    return rx.el.div(
        tab_button("Chat", "message-circle"),
        tab_button("EMS", "heart-pulse"),
        tab_button("Fire", "flame"),
        class_name="flex border-b border-gray-200 bg-white z-10 items-center px-0 sm:px-4 h-14 justify-around sm:justify-start sticky top-16",
        role="tablist",
        aria_label="Main Content Tabs",
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
            class_name="flex-grow overflow-auto",
        ),
        class_name="flex flex-col h-full w-full",
    )
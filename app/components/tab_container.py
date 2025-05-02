import reflex as rx
from app.states.ui_state import UiState
from app.states.chat_state import ChatState
from app.components.ems_form import ems_form
from app.components.fire_form import fire_form
from app.components.input_area import input_area
from app.components.message_bubble import message_bubble
from app.components.preset_cards import preset_cards


def tab_button(
    icon: str, label: str, is_active: rx.Var[bool]
) -> rx.Component:
    """Creates a button for the tab navigation."""
    base_class = "flex items-center gap-2 px-4 py-3 border-b-2 transition-colors duration-150 ease-in-out group min-h-[48px]"
    active_class = f"{base_class} border-primary text-primary bg-primary/5 dark:bg-primary/10"
    inactive_class = f"{base_class} border-transparent text-neutral dark:text-gray-400 hover:border-gray-300 dark:hover:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700/50"
    icon_class = "size-5"
    icon_active_class = f"{icon_class} text-primary"
    icon_inactive_class = f"{icon_class} text-neutral dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-300 transition-colors"
    label_class = "text-sm font-medium"
    label_active_class = f"{label_class} text-primary"
    label_inactive_class = f"{label_class} text-neutral dark:text-gray-400 group-hover:text-gray-700 dark:group-hover:text-gray-300 transition-colors"
    return rx.el.button(
        rx.icon(
            tag=icon,
            class_name=rx.cond(
                is_active,
                icon_active_class,
                icon_inactive_class,
            ),
        ),
        rx.el.span(
            label,
            class_name=rx.cond(
                is_active,
                label_active_class,
                label_inactive_class,
            ),
        ),
        on_click=lambda: UiState.set_active_tab(label),
        class_name=rx.cond(
            is_active, active_class, inactive_class
        ),
        aria_label=f"Switch to {label} tab",
        role="tab",
        aria_selected=is_active.to_string(),
    )


def chat_tab_content() -> rx.Component:
    """Content for the Chat tab."""
    return rx.el.div(
        rx.el.div(
            rx.cond(
                ChatState.messages.length() == 0,
                preset_cards(),
                rx.el.div(
                    rx.foreach(
                        ChatState.messages,
                        lambda message, index: message_bubble(
                            message["text"],
                            message["is_ai"],
                            (
                                index
                                == ChatState.messages.length()
                                - 1
                            )
                            & ChatState.typing,
                        ),
                    ),
                    class_name="flex-1 overflow-y-auto p-4 space-y-6 scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent",
                ),
            ),
            class_name="relative flex-1 overflow-hidden",
        ),
        input_area(),
        class_name="flex flex-col h-full",
    )


def tab_container() -> rx.Component:
    """Container holding the main content tabs."""
    return rx.el.div(
        rx.el.div(
            tab_button(
                "message-circle",
                "Chat",
                UiState.active_tab == "Chat",
            ),
            tab_button(
                "activity",
                "EMS",
                UiState.active_tab == "EMS",
            ),
            tab_button(
                "flame",
                "Fire",
                UiState.active_tab == "Fire",
            ),
            class_name="flex border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 sticky top-16 z-10",
            role="tablist",
        ),
        rx.el.div(
            rx.match(
                UiState.active_tab,
                ("Chat", chat_tab_content()),
                ("EMS", ems_form()),
                ("Fire", fire_form()),
                rx.el.div("Unknown Tab"),
            ),
            class_name="flex-1 overflow-hidden bg-gray-50 dark:bg-gray-900",
            role="tabpanel",
        ),
        class_name="flex flex-col h-full",
    )
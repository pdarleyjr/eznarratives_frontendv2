import reflex as rx
from app.states.session_state import SessionState, Session
from app.states.ui_state import UiState


def session_item(
    session: Session,
    is_active: rx.Var[bool],
    is_open: rx.Var[bool],
) -> rx.Component:
    """Displays a single session item in the sidebar."""
    icon_map = {
        "EMS": ("heart-pulse", "stroke-red-500"),
        "Fire": ("flame", "stroke-orange-500"),
        "Both": ("zap", "stroke-purple-500"),
        "Chat": ("message-square", "stroke-blue-500"),
    }
    icon_tag, icon_color_class = icon_map.get(
        session["type"], ("help-circle", "stroke-gray-500")
    )
    base_class = "flex items-center w-full px-3 py-2.5 rounded-lg transition-colors duration-150 ease-in-out min-h-[48px]"
    active_class = f"{base_class} bg-primary/10 dark:bg-primary/20 text-primary dark:text-primary-300 font-medium"
    inactive_class = f"{base_class} hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
    icon_base_class = "stroke-current size-5 flex-shrink-0 transition-all duration-300 ease-in-out"
    icon_position_class = rx.cond(
        is_open, "mr-3", "mx-auto"
    )
    return rx.el.button(
        rx.icon(
            tag=icon_tag,
            class_name=f"{icon_base_class} {icon_color_class} {icon_position_class}",
        ),
        rx.cond(
            is_open,
            rx.el.div(
                rx.el.p(
                    session["date"],
                    class_name="text-xs font-medium text-gray-600 dark:text-gray-400",
                    no_wrap=True,
                ),
                rx.el.p(
                    session["preview"],
                    class_name="text-sm text-gray-700 dark:text-gray-300 truncate",
                    no_wrap=True,
                ),
                class_name="overflow-hidden flex-1 text-left transition-opacity duration-150 ease-in-out",
            ),
            rx.fragment(),
        ),
        on_click=lambda: SessionState.select_session(
            session["date"]
        ),
        class_name=rx.cond(
            is_active, active_class, inactive_class
        ),
        width="100%",
        justify_content=rx.cond(is_open, "start", "center"),
        align_items="center",
        aria_label=f"Select session from {session['date']}",
        title=rx.cond(is_open, "", session["preview"]),
    )


def sidebar_toggle_button() -> rx.Component:
    """Button to toggle the sidebar collapse state, shown on desktop/tablet."""
    return rx.el.button(
        rx.icon(
            tag=rx.cond(
                UiState.is_sidebar_open,
                "panel-left-close",
                "panel-right-close",
            ),
            size=20,
            class_name="stroke-gray-600 dark:stroke-gray-400 flex-shrink-0 transition-transform duration-300 ease-in-out",
            transform=rx.cond(
                UiState.is_sidebar_open,
                "rotate(0deg)",
                "rotate(180deg)",
            ),
        ),
        rx.cond(
            UiState.is_sidebar_open,
            rx.el.span(
                "Collapse",
                class_name="text-sm font-medium text-gray-700 dark:text-gray-300 flex-1 text-left whitespace-nowrap transition-opacity duration-150 ease-in-out",
            ),
            rx.fragment(),
        ),
        on_click=UiState.toggle_sidebar,
        class_name="hidden sm:flex items-center w-full px-3 py-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-colors duration-150 ease-in-out min-h-[48px]",
        width="100%",
        justify_content=rx.cond(
            UiState.is_sidebar_open, "start", "center"
        ),
        aria_label=rx.cond(
            UiState.is_sidebar_open,
            "Collapse sidebar",
            "Expand sidebar",
        ),
        title=rx.cond(
            UiState.is_sidebar_open, "", "Expand sidebar"
        ),
    )


def sidebar() -> rx.Component:
    """Renders the collapsible sidebar."""
    sidebar_container = rx.el.aside(
        rx.el.div(
            rx.el.div(class_name="h-16 flex-shrink-0"),
            rx.el.div(
                rx.el.h3(
                    "Sessions",
                    class_name=f"text-sm font-semibold text-gray-500 dark:text-gray-400 px-4 py-2 transition-all duration-150 ease-in-out {rx.cond(UiState.is_sidebar_open, 'opacity-100', 'opacity-0 h-0 overflow-hidden')}",
                ),
                rx.el.div(
                    rx.foreach(
                        SessionState.sessions,
                        lambda session: session_item(
                            session,
                            UiState.active_session
                            == session["date"],
                            UiState.is_sidebar_open,
                        ),
                    ),
                    class_name="flex-1 overflow-y-auto space-y-1 px-2 pb-4 scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent",
                ),
                class_name="flex flex-col flex-grow overflow-hidden",
            ),
            rx.el.div(
                sidebar_toggle_button(),
                rx.el.button(
                    rx.icon(
                        tag="settings",
                        size=20,
                        class_name=f"stroke-gray-600 dark:stroke-gray-400 flex-shrink-0 transition-all duration-300 ease-in-out {rx.cond(UiState.is_sidebar_open, 'mr-3', 'mx-auto')}",
                    ),
                    rx.cond(
                        UiState.is_sidebar_open,
                        rx.el.span(
                            "Settings",
                            class_name="text-sm font-medium text-gray-700 dark:text-gray-300 flex-1 text-left whitespace-nowrap transition-opacity duration-150 ease-in-out",
                        ),
                        rx.fragment(),
                    ),
                    on_click=SessionState.open_settings,
                    class_name="flex items-center w-full px-3 py-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-colors duration-150 ease-in-out min-h-[48px]",
                    width="100%",
                    justify_content=rx.cond(
                        UiState.is_sidebar_open,
                        "start",
                        "center",
                    ),
                    aria_label="Open Settings",
                    title=rx.cond(
                        UiState.is_sidebar_open,
                        "",
                        "Settings",
                    ),
                ),
                class_name="mt-auto p-2 border-t border-gray-200 dark:border-gray-700 pb-safe-bottom flex-shrink-0 space-y-1",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=f"fixed top-0 left-0 h-screen transition-all duration-300 ease-in-out bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 shadow-md flex-shrink-0 {UiState.sidebar_width} overflow-hidden z-30",
    )
    mobile_overlay = rx.cond(
        ~UiState.is_sidebar_open,
        rx.el.div(
            on_click=UiState.toggle_sidebar,
            class_name="fixed inset-0 bg-black/30 z-20 sm:hidden",
        ),
        rx.fragment(),
    )
    return rx.fragment(sidebar_container, mobile_overlay)
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
        "EMS": ("activity", "text-red-500"),
        "Fire": ("flame", "text-orange-500"),
        "Both": ("zap", "text-purple-500"),
        "Chat": ("message-circle", "text-blue-500"),
    }
    icon_tag, icon_color = icon_map.get(
        session["type"], ("help-circle", "text-gray-500")
    )
    base_class = "flex items-center w-full px-3 py-2.5 rounded-lg transition-colors duration-150 ease-in-out min-h-[48px]"
    active_class = f"{base_class} bg-primary/10 dark:bg-primary/20 text-primary dark:text-primary-300 font-medium"
    inactive_class = f"{base_class} hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
    return rx.el.button(
        rx.icon(
            tag=icon_tag,
            size=20,
            class_name=f"{icon_color} flex-shrink-0 transition-all duration-300 ease-in-out",
            margin_x=rx.cond(is_open, "0", "auto"),
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
                class_name="ml-3 overflow-hidden flex-1 text-left",
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
        aria_label=f"Select session from {session['date']}",
    )


def sidebar() -> rx.Component:
    """Renders the collapsible sidebar."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(class_name="h-16 flex-shrink-0"),
            rx.el.div(
                rx.el.h3(
                    "Sessions",
                    class_name=rx.cond(
                        UiState.is_sidebar_open,
                        "text-sm font-semibold text-gray-500 dark:text-gray-400 px-4 py-2 transition-opacity duration-150 ease-in-out opacity-100",
                        "text-sm font-semibold text-gray-500 dark:text-gray-400 px-4 py-2 transition-opacity duration-150 ease-in-out opacity-0 pointer-events-none h-0 overflow-hidden",
                    ),
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
                rx.el.button(
                    rx.icon(
                        tag="settings",
                        size=20,
                        class_name="text-gray-600 dark:text-gray-400 flex-shrink-0 transition-all duration-300 ease-in-out",
                        margin_x=rx.cond(
                            UiState.is_sidebar_open,
                            "0",
                            "auto",
                        ),
                    ),
                    rx.cond(
                        UiState.is_sidebar_open,
                        rx.el.span(
                            "Settings",
                            class_name="ml-3 text-sm font-medium text-gray-700 dark:text-gray-300 flex-1 text-left whitespace-nowrap",
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
                ),
                class_name="mt-auto p-2 border-t border-white/20 dark:border-gray-700/30 pb-safe-bottom flex-shrink-0",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name=f"fixed top-0 left-0 h-screen transition-width duration-300 ease-in-out bg-gradient-to-b from-white/80 to-white/50 dark:from-neutral-800/80 dark:to-neutral-800/50 backdrop-blur-lg border-r border-white/20 dark:border-neutral-700/30 shadow-lg flex-shrink-0 {UiState.sidebar_width} overflow-hidden z-20",
    )
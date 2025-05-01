import reflex as rx
from app.states.session_state import SessionState
from app.states.ui_state import UiState


def session_item(session) -> rx.Component:
    """A single session item in the sidebar."""
    return rx.el.button(
        rx.el.div(
            rx.icon(
                rx.match(
                    session["type"],
                    ("EMS", "heart-pulse"),
                    ("Fire", "flame"),
                    ("Both", "combine"),
                    "message-circle",
                ),
                size=20,
                class_name=rx.cond(
                    UiState.sidebar_collapsed,
                    "mx-auto",
                    rx.match(
                        session["type"],
                        ("EMS", "text-rose-500"),
                        ("Fire", "text-red-500"),
                        ("Both", "text-purple-500"),
                        "text-blue-500",
                    ),
                ),
            ),
            rx.cond(
                ~UiState.sidebar_collapsed,
                rx.el.div(
                    rx.el.p(
                        session["date"],
                        class_name="text-xs text-gray-500",
                    ),
                    rx.el.p(
                        session["preview"],
                        class_name="text-sm text-gray-700 truncate",
                    ),
                    class_name="flex-1 overflow-hidden ml-3",
                ),
            ),
            class_name="flex flex-row items-center w-full",
        ),
        on_click=lambda: SessionState.select_session(
            session["date"]
        ),
        class_name=rx.cond(
            UiState.sidebar_collapsed,
            "flex items-center justify-center h-12 w-12 mx-auto rounded-lg hover:bg-gray-100 transition-colors duration-150 ease-in-out",
            "flex items-center px-4 py-3 rounded-lg hover:bg-gray-100 w-full text-left transition-colors duration-150 ease-in-out",
        ),
        title=session["preview"],
    )


def sidebar() -> rx.Component:
    """The main sidebar component, responsive and collapsible."""
    return rx.el.aside(
        rx.el.div(
            rx.cond(
                ~UiState.sidebar_collapsed,
                rx.el.p(
                    "EZ Narratives",
                    class_name="text-lg font-bold text-gray-800 whitespace-nowrap overflow-hidden",
                ),
                rx.el.span(),
            ),
            rx.el.button(
                rx.icon(
                    rx.cond(
                        UiState.sidebar_collapsed,
                        "panel-right-open",
                        "panel-left-close",
                    ),
                    size=20,
                ),
                on_click=UiState.toggle_sidebar_collapse,
                class_name="hidden lg:flex items-center justify-center w-8 h-8 rounded-md text-gray-500 hover:bg-gray-200 hover:text-gray-700 transition-colors",
                title=rx.cond(
                    UiState.sidebar_collapsed,
                    "Expand Sidebar",
                    "Collapse Sidebar",
                ),
            ),
            class_name="p-4 flex justify-between items-center border-b border-gray-200 h-16 flex-shrink-0",
        ),
        rx.el.div(
            rx.cond(
                ~UiState.sidebar_collapsed,
                rx.el.p(
                    "Sessions",
                    class_name="text-sm font-medium text-gray-600 px-4 pt-4 pb-2",
                ),
            ),
            rx.scroll_area(
                rx.el.div(
                    rx.foreach(
                        SessionState.sessions, session_item
                    ),
                    class_name=rx.cond(
                        UiState.sidebar_collapsed,
                        "flex flex-col items-center gap-2 p-2",
                        "flex flex-col gap-1 p-2",
                    ),
                ),
                scrollbars="vertical",
                type="auto",
                class_name="flex-grow",
            ),
            class_name="flex flex-col flex-grow overflow-hidden",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("settings", size=20),
                rx.cond(
                    ~UiState.sidebar_collapsed,
                    rx.el.span(
                        "Settings",
                        class_name="text-sm font-medium ml-3",
                    ),
                ),
                on_click=SessionState.open_settings,
                class_name=rx.cond(
                    UiState.sidebar_collapsed,
                    "flex items-center justify-center w-12 h-12 mx-auto rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-800 transition-colors",
                    "flex flex-row items-center w-full px-4 py-3 rounded-lg hover:bg-gray-100 text-gray-700 transition-colors duration-150 ease-in-out",
                ),
                title="Settings",
            ),
            class_name="p-4 border-t border-gray-200 flex-shrink-0",
        ),
        class_name=rx.cond(
            UiState.sidebar_collapsed,
            rx.cond(
                UiState.sidebar_open,
                "fixed top-0 left-0 z-30 flex flex-col h-screen bg-white shadow-lg transition-all duration-300 ease-in-out lg:w-16 translate-x-0",
                "fixed top-0 left-0 z-30 flex flex-col h-screen bg-white shadow-lg transition-all duration-300 ease-in-out lg:w-16 -translate-x-full lg:translate-x-0",
            ),
            rx.cond(
                UiState.sidebar_open,
                "fixed top-0 left-0 z-30 flex flex-col h-screen bg-white shadow-lg transition-all duration-300 ease-in-out lg:w-64 translate-x-0",
                "fixed top-0 left-0 z-30 flex flex-col h-screen bg-white shadow-lg transition-all duration-300 ease-in-out lg:w-64 -translate-x-full lg:translate-x-0",
            ),
        ),
    )
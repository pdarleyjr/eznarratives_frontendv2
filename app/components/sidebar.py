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
                    UiState.sidebar_collapsed
                    & ~UiState.sidebar_open,
                    "mx-auto text-neutral group-hover:text-primary",
                    rx.cond(
                        UiState.current_active_session
                        == session["date"],
                        "text-primary",
                        rx.match(
                            session["type"],
                            (
                                "EMS",
                                "text-rose-500 group-hover:text-rose-600",
                            ),
                            (
                                "Fire",
                                "text-red-500 group-hover:text-red-600",
                            ),
                            (
                                "Both",
                                "text-purple-500 group-hover:text-purple-600",
                            ),
                            "text-blue-500 group-hover:text-blue-600",
                        ),
                    ),
                ),
            ),
            rx.cond(
                ~(
                    UiState.sidebar_collapsed
                    & ~UiState.sidebar_open
                ),
                rx.el.div(
                    rx.el.p(
                        session["date"],
                        class_name="text-xs text-neutral",
                    ),
                    rx.el.p(
                        session["preview"],
                        class_name=rx.cond(
                            UiState.current_active_session
                            == session["date"],
                            "text-sm text-primary font-medium truncate",
                            "text-sm text-gray-700 truncate",
                        ),
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
            UiState.sidebar_collapsed
            & ~UiState.sidebar_open,
            "flex items-center justify-center h-12 w-12 mx-auto rounded-lg hover:bg-secondary transition-colors duration-150 ease-in-out group min-h-[48px]",
            rx.cond(
                UiState.current_active_session
                == session["date"],
                "flex items-center px-4 py-3 rounded-lg bg-blue-50 w-full text-left transition-colors duration-150 ease-in-out min-h-[48px]",
                "flex items-center px-4 py-3 rounded-lg hover:bg-secondary w-full text-left transition-colors duration-150 ease-in-out min-h-[48px]",
            ),
        ),
        title=session["preview"],
        aria_current=rx.cond(
            UiState.current_active_session
            == session["date"],
            "page",
            False,
        ),
    )


def sidebar_header() -> rx.Component:
    """Header section of the sidebar."""
    return rx.el.div(
        rx.el.button(
            rx.icon("x", size=24),
            on_click=UiState.toggle_sidebar,
            class_name="absolute top-4 right-4 p-2 text-neutral hover:bg-secondary rounded-md lg:hidden z-40 h-11 w-11 flex items-center justify-center",
            aria_label="Close Menu",
        ),
        rx.el.div(
            rx.cond(
                ~(
                    UiState.sidebar_collapsed
                    & ~UiState.sidebar_open
                ),
                rx.el.p(
                    "EZ Narratives",
                    class_name="text-lg font-bold text-gray-800 whitespace-nowrap overflow-hidden",
                ),
                rx.el.img(
                    src="/favicon.ico",
                    alt="EZ Narratives Logo",
                    class_name="h-8 w-8",
                ),
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
                class_name="hidden lg:flex items-center justify-center w-10 h-10 rounded-md text-neutral hover:bg-secondary hover:text-primary transition-colors",
                aria_label=rx.cond(
                    UiState.sidebar_collapsed,
                    "Expand Sidebar",
                    "Collapse Sidebar",
                ),
                aria_expanded=~UiState.sidebar_collapsed,
            ),
            class_name="flex justify-between items-center w-full",
        ),
        class_name="p-4 flex justify-between items-center border-b border-white/20 h-16 flex-shrink-0 relative",
    )


def sidebar_footer() -> rx.Component:
    """Footer section of the sidebar with Settings."""
    return rx.el.div(
        rx.el.button(
            rx.icon("settings", size=20),
            rx.cond(
                ~(
                    UiState.sidebar_collapsed
                    & ~UiState.sidebar_open
                ),
                rx.el.span(
                    "Settings",
                    class_name="text-sm font-medium ml-3",
                ),
            ),
            on_click=SessionState.open_settings,
            class_name=rx.cond(
                UiState.sidebar_collapsed
                & ~UiState.sidebar_open,
                "flex items-center justify-center w-12 h-12 mx-auto rounded-lg text-neutral hover:bg-secondary hover:text-primary transition-colors min-h-[48px]",
                "flex flex-row items-center w-full px-4 py-3 rounded-lg hover:bg-secondary text-neutral hover:text-primary transition-colors duration-150 ease-in-out min-h-[48px]",
            ),
            title="Settings",
        ),
        class_name="p-4 border-t border-white/20 flex-shrink-0",
    )


def sidebar() -> rx.Component:
    """The main sidebar component, responsive and collapsible with glass effect."""
    sidebar_base_class = "fixed top-0 left-0 z-30 flex flex-col h-screen transition-all duration-300 ease-in-out bg-gradient-to-b from-white/30 to-white/10 backdrop-blur-md border-r border-white/20 shadow-lg"
    sidebar_width_class = rx.cond(
        UiState.sidebar_collapsed, "lg:w-16", "lg:w-64"
    )
    sidebar_mobile_transform_class = rx.cond(
        UiState.sidebar_open,
        "translate-x-0 animate-slide-in-left",
        "-translate-x-full lg:translate-x-0 animate-slide-out-left",
    )
    return rx.el.aside(
        sidebar_header(),
        rx.el.div(
            rx.cond(
                ~(
                    UiState.sidebar_collapsed
                    & ~UiState.sidebar_open
                ),
                rx.el.p(
                    "Sessions",
                    class_name="text-sm font-semibold text-neutral px-4 pt-4 pb-2 tracking-wide",
                ),
            ),
            rx.scroll_area(
                rx.el.div(
                    rx.foreach(
                        SessionState.sessions, session_item
                    ),
                    class_name=rx.cond(
                        UiState.sidebar_collapsed
                        & ~UiState.sidebar_open,
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
        sidebar_footer(),
        class_name=f"{sidebar_base_class} {sidebar_width_class} {sidebar_mobile_transform_class} w-64",
        aria_label="Main Navigation",
    )
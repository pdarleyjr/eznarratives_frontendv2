import reflex as rx
from app.states.session_state import SessionState
from app.states.ui_state import UiState


def session_item(session) -> rx.Component:
    """A single session item in the sidebar."""
    is_active = (
        UiState.current_active_session == session["date"]
    )
    is_collapsed_desktop = UiState.sidebar_collapsed
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
                    is_collapsed_desktop,
                    rx.cond(
                        is_active,
                        "text-primary",
                        "text-neutral group-hover:text-primary",
                    ),
                    rx.cond(
                        is_active,
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
                ~is_collapsed_desktop,
                rx.el.div(
                    rx.el.p(
                        session["date"],
                        class_name="text-xs text-neutral whitespace-nowrap",
                    ),
                    rx.el.p(
                        session["preview"],
                        class_name=rx.cond(
                            is_active,
                            "text-sm text-primary font-medium truncate whitespace-nowrap",
                            "text-sm text-gray-700 truncate whitespace-nowrap",
                        ),
                    ),
                    class_name="flex-1 overflow-hidden ml-3 text-left",
                ),
            ),
            class_name=rx.cond(
                is_collapsed_desktop,
                "flex items-center justify-center w-full h-full",
                "flex flex-row items-center w-full",
            ),
        ),
        on_click=lambda: SessionState.select_session(
            session["date"]
        ),
        class_name=rx.cond(
            is_collapsed_desktop,
            rx.cond(
                is_active,
                "flex items-center justify-center h-12 w-12 mx-auto rounded-lg bg-blue-100 transition-colors duration-150 ease-in-out group min-h-[48px]",
                "flex items-center justify-center h-12 w-12 mx-auto rounded-lg hover:bg-secondary transition-colors duration-150 ease-in-out group min-h-[48px]",
            ),
            rx.cond(
                is_active,
                "flex items-center px-4 py-3 rounded-lg bg-blue-50 w-full text-left transition-colors duration-150 ease-in-out min-h-[48px]",
                "flex items-center px-4 py-3 rounded-lg hover:bg-secondary w-full text-left transition-colors duration-150 ease-in-out min-h-[48px]",
            ),
        ),
        title=rx.cond(
            is_collapsed_desktop,
            f"{session['type']} - {session['date']}",
            session["preview"],
        ),
        aria_current=rx.cond(is_active, "page", False),
    )


def sidebar_header() -> rx.Component:
    """Header section of the sidebar."""
    return rx.el.div(
        rx.el.div(
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
                class_name="hidden lg:flex items-center justify-center w-10 h-10 rounded-md text-neutral hover:bg-white/20 hover:text-primary transition-colors",
                aria_label=rx.cond(
                    UiState.sidebar_collapsed,
                    "Expand Sidebar",
                    "Collapse Sidebar",
                ),
                aria_expanded=~UiState.sidebar_collapsed,
            ),
            rx.el.button(
                rx.icon("x", size=24),
                on_click=UiState.toggle_sidebar,
                class_name="p-2 text-neutral hover:bg-white/20 rounded-md lg:hidden h-11 w-11 flex items-center justify-center",
                aria_label="Close Menu",
            ),
            class_name=rx.cond(
                UiState.sidebar_collapsed,
                "flex justify-center w-full",
                "flex justify-end lg:justify-start w-full",
            ),
        ),
        class_name="p-4 flex justify-between items-center border-b border-white/20 h-16 flex-shrink-0 relative z-50",
    )


def sidebar_footer() -> rx.Component:
    """Footer section of the sidebar with Settings."""
    is_collapsed_desktop = UiState.sidebar_collapsed
    is_active = False
    return rx.el.div(
        rx.el.button(
            rx.icon(
                "settings",
                size=20,
                class_name=rx.cond(
                    is_collapsed_desktop,
                    "text-neutral group-hover:text-primary",
                    "text-neutral group-hover:text-primary",
                ),
            ),
            rx.cond(
                ~is_collapsed_desktop,
                rx.el.span(
                    "Settings",
                    class_name="text-sm font-medium ml-3",
                ),
            ),
            on_click=SessionState.open_settings,
            class_name=rx.cond(
                is_collapsed_desktop,
                rx.cond(
                    is_active,
                    "flex items-center justify-center h-12 w-12 mx-auto rounded-lg bg-blue-100 transition-colors duration-150 ease-in-out group min-h-[48px]",
                    "flex items-center justify-center h-12 w-12 mx-auto rounded-lg hover:bg-secondary transition-colors duration-150 ease-in-out group min-h-[48px]",
                ),
                rx.cond(
                    is_active,
                    "flex flex-row items-center w-full px-4 py-3 rounded-lg bg-blue-50 text-primary transition-colors duration-150 ease-in-out min-h-[48px]",
                    "flex flex-row items-center w-full px-4 py-3 rounded-lg hover:bg-secondary text-neutral hover:text-primary transition-colors duration-150 ease-in-out min-h-[48px]",
                ),
            ),
            title="Settings",
        ),
        class_name="p-4 border-t border-white/20 flex-shrink-0",
    )


def sidebar() -> rx.Component:
    """The main sidebar component, responsive and collapsible with glass effect."""
    sidebar_base_class = "fixed top-0 left-0 z-50 flex flex-col h-screen transition-all duration-300 ease-in-out bg-gradient-to-b from-white/80 to-white/60 dark:from-gray-900/80 dark:to-gray-900/60 backdrop-blur-lg border-r border-white/20 dark:border-gray-700/50 shadow-lg"
    sidebar_width_class = rx.cond(
        UiState.sidebar_collapsed, "lg:w-20", "lg:w-64"
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
                ~UiState.sidebar_collapsed,
                rx.el.p(
                    "Sessions",
                    class_name="text-xs font-semibold text-neutral px-4 pt-4 pb-2 tracking-wider uppercase",
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
                class_name="flex-grow h-full",
            ),
            class_name="flex flex-col flex-grow overflow-hidden pt-0",
        ),
        sidebar_footer(),
        class_name=f"{sidebar_base_class} {sidebar_width_class} {sidebar_mobile_transform_class} w-64",
        aria_label="Main Navigation",
        id="main-sidebar",
    )
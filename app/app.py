import reflex as rx
from app.components.sidebar import sidebar
from app.components.tab_container import tab_container
from app.states.ui_state import UiState


def index() -> rx.Component:
    """The main app page."""
    return rx.el.div(
        sidebar(),
        rx.cond(
            UiState.sidebar_open,
            rx.el.div(
                on_click=UiState.toggle_sidebar,
                class_name="fixed inset-0 bg-black/30 z-20 lg:hidden transition-opacity duration-300 ease-in-out opacity-100",
            ),
            rx.el.div(
                class_name="fixed inset-0 z-20 lg:hidden transition-opacity duration-300 ease-in-out opacity-0 pointer-events-none"
            ),
        ),
        rx.el.main(
            tab_container(),
            class_name=rx.cond(
                UiState.sidebar_collapsed,
                "flex-1 overflow-hidden transition-all duration-300 ease-in-out lg:ml-16",
                "flex-1 overflow-hidden transition-all duration-300 ease-in-out lg:ml-64",
            ),
        ),
        class_name="flex h-screen bg-gray-50",
    )


page_meta = [
    {"name": "theme-color", "content": "#FFFFFF"},
    {
        "name": "apple-mobile-web-app-capable",
        "content": "yes",
    },
    {
        "name": "apple-mobile-web-app-status-bar-style",
        "content": "default",
    },
    {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, viewport-fit=cover",
    },
]
app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/styles.css"],
)
app.add_page(index, route="/", meta=page_meta)
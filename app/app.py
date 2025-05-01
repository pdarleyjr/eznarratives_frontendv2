import reflex as rx
from app.components.sidebar import sidebar
from app.components.tab_container import tab_container
from app.states.ui_state import UiState


def index() -> rx.Component:
    """The main app page."""
    return rx.el.div(
        sidebar(),
        rx.cond(
            UiState.sidebar_open
            & ~UiState.sidebar_collapsed,
            rx.el.div(
                on_click=UiState.toggle_sidebar,
                class_name="fixed inset-0 bg-black/50 z-40 lg:hidden transition-opacity duration-300 ease-in-out opacity-100 animate-fade-in",
            ),
            rx.el.div(
                class_name="fixed inset-0 z-40 lg:hidden transition-opacity duration-300 ease-in-out opacity-0 pointer-events-none"
            ),
        ),
        rx.el.main(
            tab_container(),
            class_name=rx.cond(
                UiState.sidebar_collapsed,
                "flex-1 overflow-hidden transition-all duration-300 ease-in-out lg:ml-20",
                "flex-1 overflow-hidden transition-all duration-300 ease-in-out lg:ml-64",
            ),
        ),
        class_name="flex h-screen bg-gray-100",
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
    {
        "rel": "apple-touch-icon",
        "sizes": "180x180",
        "href": "/apple-touch-icon.png",
    },
    {
        "rel": "icon",
        "type": "image/png",
        "sizes": "32x32",
        "href": "/favicon-32x32.png",
    },
    {
        "rel": "icon",
        "type": "image/png",
        "sizes": "16x16",
        "href": "/favicon-16x16.png",
    },
    {"rel": "manifest", "href": "/site.webmanifest"},
    {
        "rel": "mask-icon",
        "href": "/safari-pinned-tab.svg",
        "color": "#5B3FEA",
    },
    {
        "name": "msapplication-TileColor",
        "content": "#5B3FEA",
    },
]
theme = rx.theme(
    appearance="light",
    accent_color="blue",
    gray_color="slate",
    radius="medium",
)
app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/styles.css"],
)
app.add_page(index, route="/", meta=page_meta)
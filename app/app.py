import reflex as rx
from app.components.sidebar import sidebar
from app.components.tab_container import tab_container
from app.components.header import header
from app.states.ui_state import UiState
import os


def index() -> rx.Component:
    """The main page layout."""
    return rx.el.div(
        rx.el.title("EZ Narratives"),
        rx.el.meta(
            name="description",
            content="Generate compliant EMS and Fire reports with AI assistance.",
        ),
        rx.el.meta(
            name="viewport",
            content="width=device-width, initial-scale=1.0, viewport-fit=cover",
        ),
        rx.el.meta(
            name="apple-mobile-web-app-capable",
            content="yes",
        ),
        rx.el.meta(
            name="apple-mobile-web-app-status-bar-style",
            content="default",
        ),
        rx.el.link(
            rel="apple-touch-icon",
            sizes="180x180",
            href="/apple-touch-icon.png",
        ),
        rx.el.link(rel="manifest", href="/manifest.json"),
        header(),
        rx.el.div(
            sidebar(),
            rx.el.main(
                tab_container(),
                class_name=rx.cond(
                    UiState.is_sidebar_open,
                    "transition-margin duration-300 ease-in-out md:ml-64 mt-16",
                    "transition-margin duration-300 ease-in-out md:ml-16 mt-16",
                ),
                padding_top="1rem",
            ),
            class_name="flex min-h-screen",
        ),
        rx.toast.provider(),
        class_name=rx.cond(
            UiState.theme_appearance == "dark",
            "dark bg-neutral-900",
            "bg-background",
        )
        + " min-h-screen",
    )


app_theme = rx.theme(
    accent_color="indigo",
    gray_color="slate",
    radius="medium",
    appearance=UiState.theme_appearance,
)
app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/styles.css"],
)
app.add_page(index, route="/", title="EZ Narratives")
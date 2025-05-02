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
                class_name=f"flex-1 overflow-auto bg-background dark:bg-gray-900 mt-16 transition-all duration-300 ease-in-out {UiState.main_content_margin} z-10",
                padding_top="env(safe-area-inset-top)",
            ),
            class_name="flex h-full",
        ),
        rx.toast.provider(z_index=40),
        class_name=rx.cond(
            UiState.theme_appearance == "dark",
            "dark bg-gray-900",
            "bg-background",
        )
        + " min-h-screen font-sans",
        id="app-root",
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
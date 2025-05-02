import reflex as rx
from typing import Literal

ThemeAppearance = Literal["light", "dark"]


class UiState(rx.State):
    """State for managing UI elements like sidebar and theme."""

    is_sidebar_open: bool = True
    active_tab: str = "Chat"
    active_session: str | None = None
    theme_appearance: ThemeAppearance = "light"

    @rx.var
    def sidebar_width(self) -> str:
        """Returns the Tailwind width class for the sidebar.
        Collapses to w-14 (56px) on sm+ screens, hides completely (w-0) on mobile.
        """
        return rx.cond(
            self.is_sidebar_open, "w-64", "sm:w-14 w-0"
        )

    @rx.var
    def main_content_margin(self) -> str:
        """Returns the Tailwind margin class for the main content area.
        Adjusts based on sidebar width.
        """
        return rx.cond(
            self.is_sidebar_open, "sm:ml-64", "sm:ml-14"
        )

    @rx.event
    def toggle_sidebar(self):
        """Toggles the sidebar open/closed."""
        self.is_sidebar_open = not self.is_sidebar_open

    @rx.event
    def set_active_tab(self, tab_name: str):
        """Sets the currently active tab."""
        if self.active_tab != tab_name:
            self.active_tab = tab_name

    @rx.event
    def set_active_session(self, session_date: str | None):
        """Sets the active session, updating the UI."""
        if self.active_session != session_date:
            self.active_session = session_date

    @rx.event
    def toggle_theme(self):
        """Toggles the theme between light and dark."""
        self.theme_appearance = (
            "dark"
            if self.theme_appearance == "light"
            else "light"
        )
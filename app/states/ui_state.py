import reflex as rx


class UiState(rx.State):
    """State to manage UI elements like tabs and sidebar visibility."""

    active_tab: str = "Chat"
    active_session_date: str | None = None
    sidebar_open: bool = False
    sidebar_collapsed: bool = True

    @rx.var
    def current_active_session(self) -> str | None:
        """Return the currently active session date."""
        return self.active_session_date

    @rx.event
    def toggle_sidebar(self):
        """Toggle the sidebar visibility for mobile overlay."""
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def toggle_sidebar_collapse(self):
        """Toggle the sidebar collapse state for desktop."""
        self.sidebar_collapsed = not self.sidebar_collapsed

    @rx.event
    def set_active_tab(self, tab: str):
        """Set the active tab."""
        self.active_tab = tab

    @rx.event
    def set_active_session(self, session_date: str | None):
        """Set the active session."""
        self.active_session_date = session_date
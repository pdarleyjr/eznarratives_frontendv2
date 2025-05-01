import reflex as rx


class UiState(rx.State):
    """State to manage UI elements like tabs and sidebar visibility."""

    active_tab: str = "Chat"
    sidebar_open: bool = True
    sidebar_collapsed: bool = False

    @rx.event
    def toggle_sidebar(self):
        """Toggle the sidebar visibility for mobile overlay."""
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def toggle_sidebar_collapse(self):
        """Toggle the sidebar collapse state for desktop."""
        self.sidebar_collapsed = not self.sidebar_collapsed
        if not self.sidebar_collapsed:
            self.sidebar_open = True

    @rx.event
    def set_active_tab(self, tab: str):
        """Set the active tab."""
        self.active_tab = tab
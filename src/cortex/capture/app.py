"""Cortex — single-terminal capture & search app.

One process, one terminal window. Screens are pushed/popped on a stack —
no new windows or panes are ever opened.
"""

from textual.app import App

from cortex.capture.main_menu import MainMenuScreen


class CortexApp(App):
    """Root app. Always starts on the main menu."""

    CSS_PATH = None  # add a .tcss file here later if you want custom styling
    TITLE = "Cortex"

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())


if __name__ == "__main__":
    CortexApp().run()

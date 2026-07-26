from cortex.capture.chat_screen import SearchNotesScreen
from cortex.capture.note_screen import TakeNotesScreen
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, ListView, Static, ListItem

class MainMenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(
            ListItem(Static("1. Take Notes"), id="take-notes"),
            ListItem(Static("2. Search Notes"), id="search-notes"),
            ListItem(Static("3. Exit"), id="exit"),
            id="menu-list",
        )
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id
        if item_id == "take-notes":
            self.action_take_notes()
        if item_id == "search-notes":
            self.action_search_notes()

    def action_take_notes(self):
        self.app.push_screen(TakeNotesScreen())

    def action_search_notes(self):
        self.app.push_screen(SearchNotesScreen())

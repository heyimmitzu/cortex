from datetime import datetime
from pstats import Stats
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Collapsible, Header, Footer, Input, Label, ListView, ListView, Static, ListItem, TextArea

class SearchNotesScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="search-container"):
            yield Label("cortex-search")
            yield TextArea(id="llm-reply")
            yield Collapsible(collapsed=True, id="source-list")
            yield Input(placeholder="Ask something about your meetings....")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id
        if item_id == "take-notes":
            self.action_take_notes()

    def action_take_notes(self):
        yield Static("Notes")

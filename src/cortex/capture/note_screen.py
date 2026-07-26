from datetime import datetime
from pstats import Stats
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Input, Label, ListView, ListView, Static, ListItem, TextArea

class TakeNotesScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="notes-container"):
            yield Label(f"Started {datetime.now():%Y-%m-%d %H:%M}")
            yield Input(placeholder="Meeting title.....", id="meeting-title")
            yield Label("Key Facts (live, during meeting)")
            yield TextArea(id="key-facts")
            yield Label("Brain Dump (right after the meeting)")
            yield TextArea(id="brain-dump")
        yield Footer()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        item_id = event.item.id
        if item_id == "take-notes":
            self.action_take_notes()

    def action_take_notes(self):
        yield Static("Notes")

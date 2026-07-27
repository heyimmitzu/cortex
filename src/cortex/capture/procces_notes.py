from datetime import date, datetime
from pstats import Stats
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Input, Label, ListView, ListView, Static, ListItem, TextArea

class ProcessNotesScreen(Screen):
    CSS_PATH = "process_notes.tcss"

    def __init__(self, title: str, key_facts: str, brain_dump:  str) -> None:
        super().__init__()
        self.notes_title = title
        self.raw_key_facts = key_facts
        self.raw_brain_dump = brain_dump
        self.timestamp = datetime.now()

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="processed-container"):
            yield Label("Meeting title")
            yield Input(value=self.notes_title, id="meeting-title")
            yield Label(f"Started {self.timestamp:%Y-%m-%d %H:%M}")
            yield Label("Summary (1-2 sentences)")
            yield TextArea(id="meeting-summary")
            yield Label("Key Facts")
            yield TextArea(id="key-facts")
            yield Label("Action items")
            yield TextArea(id="action-items")
            yield Label("Open questions")
            yield TextArea(id="open-questions")
        yield Footer()

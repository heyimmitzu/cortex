from datetime import datetime
from pstats import Stats
from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Input, Label, ListView, ListView, Static, ListItem, TextArea
from cortex.capture.procces_notes import ProcessNotesScreen


class TakeNotesScreen(Screen):
    BINDINGS = [
            ("ctrl+g", "process_notes", "Save & process"),
            ("escape", "pop_screen", "Back"),
        ]
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

    def action_process_notes(self) -> None:
        title = self.query_one("#meeting-title", Input).value
        key_facts = self.query_one("#key-facts", TextArea).text
        brain_dump = self.query_one("#brain-dump", TextArea).text
        self.app.push_screen(ProcessNotesScreen(title=title, key_facts=key_facts, brain_dump=brain_dump))

    def action_pop_screen(self) -> None:
        self.app.pop_screen()

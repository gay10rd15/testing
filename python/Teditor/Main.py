import argparse
from pathlib import Path

from textual import events
from textual.app import App
from textual.containers import Vertical
from textual.widgets import Input, Static
from textual.widgets._text_area import TextArea

Binds = """save ctrl+s"""
Top = """"""

Parser = argparse.ArgumentParser()
Parser.add_argument("Path", help="the path of the file you want to open", nargs="?")
args = Parser.parse_args()

cwd = Path.cwd()


def openfile(self):
    if args.Path:
        with open(args.Path, "r") as F:
            try:
                self.Ta.load_text(F.read())
            except UnicodeDecodeError:
                args.Path = None


class Ted(App):
    BINDINGS = [("ctrl+c", "quit", "Quit")]  # noqa: RUF012
    CSS_PATH = "ted.tcss"

    def compose(self):
        with Vertical():
            yield Static(Top)
            self.Ta = TextArea()
            yield self.Ta
            yield Input(placeholder="File path", id="fp")
            yield Static(Binds)
            self.Ta.tab_behavior = "indent"

    def on_mount(self):
        openfile(self)

        self.fp = self.query_one("#fp")
        self.fp.display = False

    def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+s" and "save".lower() in Binds.lower():
            if args.Path:
                try:
                    with open(args.Path, "w") as F:
                        F.write(self.Ta.text)
                        self.notify("Saved!")
                except PermissionError:
                    self.notify("Permission Error, Try something else")

            else:
                self.fp.display = True
                # pyrefly: ignore [missing-attribute]
                self.fp.value = str(cwd)
                self.set_focus(self.fp)

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "fp":
            self.fp.display = False
            # pyrefly: ignore [missing-attribute]
            pof = self.fp.value
            pof = pof.replace("~", str(Path.home()))
            self.notify(pof)

            with open(pof, "w") as F:
                F.write(self.Ta.text)

            args.Path = pof


if __name__ == "__main__":
    Ted().run()

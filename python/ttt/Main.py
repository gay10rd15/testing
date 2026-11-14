from textual.app import App
from textual.containers import Container
from textual.widgets import Button


class Main(App):
    CSS_PATH = "Main.tcss"

    def compose(self):
        with Container(id="grid"):
            yield Button()
            yield Button()
            yield Button()
            yield Button()
            yield Button()
            yield Button()
            yield Button()
            yield Button()
            yield Button()


if __name__ == "__main__":
    Main().run()

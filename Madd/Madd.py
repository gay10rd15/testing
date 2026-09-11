import io
import sys
from pathlib import Path

import crossfiledialog
import music_tag
from crossfiledialog.osascript import OsascriptException
from PIL import Image as PILimage
from PIL import UnidentifiedImageError
from textual.app import App
from textual.containers import Container, VerticalScroll
from textual.widgets import Button, Footer, Input, Static
from textual_image.widget import Image

imgpath = Path(__file__).parent / "None.png"


def updatei(self) -> None:
    self.son.update(f"""current file: {self.mf}
    song name: {self.fmf["title"]}  artist: {self.fmf["artist"]} | album: {self.fmf["album"]}""")


class Main(App):
    BINDINGS = [("ctrl+c", "quit", "Quit"), ("ctrl+o", "open", "Open")]  # noqa: RUF012
    CSS_PATH = "Madd.tcss"

    def __init__(self):
        super().__init__()
        try:
            self.mf = crossfiledialog.open_file(filter=["*.mp3", "*.wav"])
        except OsascriptException:
            sys.exit()
        self.fmf = music_tag.load_file(self.mf)
        # pyrefly: ignore [unsupported-operation]
        self.art = self.fmf["artwork"]
        try:
            self.img = PILimage.open(io.BytesIO(self.art.first.data))
        except AttributeError:
            with open(imgpath, "rb") as i:
                self.img = PILimage.open(io.BytesIO(i.read()))

    async def on_mount(self) -> None:
        updatei(self)

    def compose(self):
        self.son = Static("no file selected")
        yield Footer()

        with Container(id="inputs"):
            with VerticalScroll():
                yield self.son
            self.imgw = Image()
            self.imgw.image = self.img
            yield self.imgw
            yield Input(placeholder="Enter artist name", id="artist")
            yield Input(placeholder="Enter song name", id="name")
            yield Input(placeholder="add album", id="album")
            yield Input(placeholder="Enter genre", id="genre")
            yield Button("add album cover", id="cover")
            yield Button("reset track number", id="rtn")

    def on_input_submitted(self, event: Input.Submitted):
        if event.input.id == "artist" and self.fmf:
            self.fmf["artist"] = event.value
            self.fmf.save()
        if event.input.id == "name" and self.fmf:
            self.fmf["title"] = event.value
            self.fmf.save()
        if event.input.id == "album" and self.fmf:
            self.fmf["album"] = event.value
            self.fmf.save()
        if event.input.id == "genre" and self.fmf:
            self.fmf["genre"] = event.value
            self.fmf.save()

        updatei(self)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "cover" and self.fmf:
            try:
                image = crossfiledialog.open_file(
                    filter=["*.png", "*.jpeg", "*.svg", "*.heic", "*.webp"]
                )
                with open(image, "rb") as img_data:
                    artwork_bytes = img_data.read()
                self.fmf["artwork"] = artwork_bytes
            except OsascriptException:
                pass
            try:
                # pyrefly: ignore [unbound-name]
                self.img = PILimage.open(io.BytesIO(artwork_bytes))
            except (
                AttributeError,
                UnidentifiedImageError,
                OSError,
                UnboundLocalError,
            ):
                with open("None.png", "rb") as i:
                    self.img = PILimage.open(io.BytesIO(i.read()))
            self.imgw.image = self.img
            self.imgw.refresh()

        if event.button.id == "rtn" and self.fmf:
            self.fmf.raw["tracknumber"] = ""
        if self.fmf:
            self.fmf.save()
        updatei(self)

    def action_open(self):
        try:
            self.mf = crossfiledialog.open_file(filter=["*.mp3", "*.wav"])
        except OsascriptException:
            sys.exit()
        updatei(self)
        self.fmf = music_tag.load_file(self.mf)


if __name__ == "__main__":
    Main().run()

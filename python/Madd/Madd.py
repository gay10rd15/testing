import io
import sys
from pathlib import Path

import crossfiledialog
import music_tag
from crossfiledialog.osascript import OsascriptException
from PIL import Image as PILimage
from PIL import UnidentifiedImageError
from textual.app import App
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.theme import Theme
from textual.widgets import Button, Footer, Static, TextArea
from textual_image.widget.sixel import Image


class Ta(TextArea):
    BINDINGS = [Binding("enter", "submit", "Submit", show=False, priority=True)]  # noqa: RUF012

    class Submitted(Message, bubble=True):
        def __init__(self, text: str, control: Ta) -> None:
            super().__init__()
            self.text = text
            self._control = control

        @property
        def control(self):
            return self._control

    async def action_submit(self) -> None:
        self.post_message(self.Submitted(self.text, self))


imgpath = Path(__file__).parent / "None.png"

filters = ["*.mp3", "*.wav", "*.mp4", "*.m4a", "*.flac"]

purple_theme = Theme(
    name="Purple", background="#2c2c2e", primary="#582fe9", surface="#2c2c2c"
)


def updatei(self) -> None:
    self.mc.update(f"""current file: {self.mf}
    song name: {self.fmf["title"]}  artist: {self.fmf["artist"]} | album: {self.fmf["album"]} | genre: {self.fmf["genre"]}""")


class Main(App):
    BINDINGS = [  # noqa: RUF012
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+o", "open", "Open"),
        Binding("r", "refresh", "Refresh", show=False),
    ]
    CSS_PATH = "Madd.tcss"

    def action_refresh(self):
        self.refresh()

    def __init__(self):
        super().__init__()
        try:
            self.mf = crossfiledialog.open_file(filter=filters)
        except OsascriptException:
            sys.exit()
        self.fmf = music_tag.load_file(self.mf)
        try:
            # pyrefly: ignore [unsupported-operation]
            self.art = self.fmf["artwork"]
        except KeyError:
            self.art = None
        try:
            # pyrefly: ignore [missing-attribute]
            self.img = PILimage.open(io.BytesIO(self.art.first.data))
        except AttributeError:
            with open(imgpath, "rb") as i:
                self.img = PILimage.open(io.BytesIO(i.read()))

        self.register_theme(purple_theme)
        self.theme = "Purple"

    async def on_mount(self) -> None:
        # pyrefly: ignore [unsupported-operation]
        self.query_one("#artist", Ta).text = str(self.fmf["artist"])
        # pyrefly: ignore [unsupported-operation]
        self.query_one("#name", Ta).text = str(self.fmf["title"])
        # pyrefly: ignore [unsupported-operation]
        self.query_one("#album", Ta).text = str(self.fmf["album"])
        # pyrefly: ignore [unsupported-operation]
        self.query_one("#genre", Ta).text = str(self.fmf["genre"])
        updatei(self)

    def compose(self):
        self.log.info("son")
        yield Footer()
        self.mc = Static("no file selected")
        self.imgw = Image()
        self.imgw.can_focus = False
        self.imgw.image = self.img
        with Horizontal():
            with Vertical():
                yield self.mc
                with Horizontal():
                    yield Ta(placeholder="Enter artist name", id="artist")
                    yield Ta(placeholder="Enter song name", id="name")
                    yield Ta(placeholder="add album", id="album")
                with Horizontal():
                    yield Ta(placeholder="Enter genre", id="genre")
                    yield Button("add album cover", id="cover")
                    yield Button("reset track number", id="rtn")
            yield self.imgw

    def on_ta_submitted(self, event: Ta.Submitted):
        if event.control.id == "artist" and self.fmf:
            self.fmf["artist"] = event.text
            self.fmf.save()
        elif event.control.id == "name" and self.fmf:
            self.fmf["title"] = event.text
            self.fmf.save()
        elif event.control.id == "album" and self.fmf:
            self.fmf["album"] = event.text
            self.fmf.save()
        elif event.control.id == "genre" and self.fmf:
            self.fmf["genre"] = event.text
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
                self.img = PILimage.open(io.BytesIO(artwork_bytes))

            except (
                OsascriptException,
                AttributeError,
                UnidentifiedImageError,
                OSError,
                UnboundLocalError,
            ):
                imgpath = Path(__file__).parent / "None.png"
                with open(imgpath, "rb") as i:
                    artwork_bytes = i.read()
                    self.img = PILimage.open(io.BytesIO(artwork_bytes))
            self.imgw.image = self.img
            self.imgw.refresh()
            updatei(self)

        if event.button.id == "rtn" and self.fmf:
            self.fmf.raw["tracknumber"] = None
        if self.fmf:
            self.fmf.save()
        updatei(self)

    def action_open(self):
        try:
            self.mf = crossfiledialog.open_file(filter=filters)
        except OsascriptException:
            sys.exit()
        self.fmf = music_tag.load_file(self.mf)
        try:
            # pyrefly: ignore [unsupported-operation]
            self.art = self.fmf["artwork"]
            self.img = PILimage.open(io.BytesIO(self.art.first.data))
        except KeyError, AttributeError:
            with open(imgpath, "rb") as i:
                self.img = PILimage.open(io.BytesIO(i.read()))
        self.imgw.image = self.img
        self.imgw.refresh()
        # pyrefly: ignore [unsupported-operation]
        self.query_one("#artist", Ta).text = str(self.fmf["artist"])
        # pyrefly: ignore [unsupported-operation]
        self.query_one("#name", Ta).text = str(self.fmf["title"])
        # pyrefly: ignore [unsupported-operation]
        self.query_one("#album", Ta).text = str(self.fmf["album"])
        # pyrefly: ignore [unsupported-operation]
        self.query_one("#genre", Ta).text = str(self.fmf["genre"])
        updatei(self)


if __name__ == "__main__":
    Main().run()

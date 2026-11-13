import argparse
import os
import sqlite3
import subprocess
from time import sleep

import messages
from textual import work
from textual.app import App
from textual.containers import Horizontal, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Label, ListItem, ListView, Static


def get_chat_guid(chat_id):
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT guid FROM chat WHERE rowid = ?", (chat_id,)).fetchone()
    conn.close()
    return row[0] if row else None


def send_to_chat(chat_num: str, message: str):
    guid = get_chat_guid(chat_num)
    if not guid:
        raise ValueError(f"Could not find a chat session with ID: {chat_num}")
    escaped_message = message.replace("\\", "\\\\").replace('"', '\\"')
    script = f'''
    tell application "Messages"
        set theChat to chat id "{guid}"
        send "{escaped_message}" to theChat
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True)


db = messages.get_db()

parser = argparse.ArgumentParser(
    prog="Py-Message",
    description="A replacement for the imessage app",
    epilog="Only works on Mac",
)
parser.add_argument("-L", "--Lines")
parser.add_argument("-C", "--Chat_Num")
args = parser.parse_args()

nl = args.Lines if args.Lines else 10
cn = args.Chat_Num if args.Chat_Num else None


nl = int(args.Lines) if args.Lines else None


def readm(chat_num, lines):
    full_convo = []
    if lines:
        msgs = db.messages(chat_id=chat_num, limit=lines, reverse=True)
    else:
        msgs = db.messages(chat_id=chat_num, reverse=True)
    for msg in msgs:
        if msg.is_from_me:
            sender = "me"
        elif msg.sender is not None:
            sender = msg.sender.display_name
        else:
            sender = "unknown"
        full_convo.append(f"{sender}: {msg.text}")
    return "\n".join(reversed(full_convo))


class MainC(Screen):
    CSS_PATH = "Main.tcss"
    BINDINGS = [("c", "cc", "Change chat"), ("r", "refresh", "Refresh")]  # noqa: RUF012

    def compose(self):

        yield Footer()
        with VerticalScroll(
            id="chat",
        ):
            yield Static(id="convo")
        with Horizontal():
            yield Button("+")
            yield Input(placeholder="what do you want to say")

    def on_input_submitted(self, event: Input.Submitted):
        # pyrefly: ignore [missing-attribute]
        self._send(self.app.chat_num, event.value)
        event.input.clear()
        self.notify("done")

    def on_mount(self):
        self._refresh()

    def on_screen_resume(self):
        self._refresh()
        self.query_one("#chat", VerticalScroll).scroll_end(animate=False)

    def _refresh(self):
        # pyrefly: ignore [missing-attribute]
        convo = readm(self.app.chat_num, nl)
        self.query_one("#convo", Static).update(convo)
        scroll = self.query_one("#chat", VerticalScroll)
        self.call_after_refresh(scroll.scroll_end, animate=False)

    def action_cc(self):
        self.app.push_screen("cc")

    @work(thread=True)
    def _send(self, chat_num: str, message: str):
        send_to_chat(chat_num, message)
        sleep(1.0)
        self.app.call_from_thread(self._refresh)
        self.query_one("#chat", VerticalScroll).scroll_end(animate=False)

    def action_refresh(self):
        self._refresh()


class Change_chat(Screen):
    BINDINGS = [("escape", "cancel", "Cancel")]  # noqa: RUF012

    def on_mount(self):
        list_view = self.query_one("#List", ListView)
        for chat in db.chats():
            list_view.append(
                ListItem(Label(f"{chat.id}: {chat.display_name or chat.identifier}"))
            )

    def compose(self):
        yield Footer()
        yield ListView(id="List")

    def action_cancel(self):
        self.app.pop_screen()

    def on_list_view_selected(self, event: ListView.Selected):
        si = event.item
        label = si.query_one(Label)
        content = str(label.content)
        # pyrefly: ignore [missing-attribute]
        self.app.chat_num = content.split(":")[0]
        self.app.pop_screen()


class Main(App):
    SCREENS = {"Main": MainC, "cc": Change_chat}  # noqa: RUF012

    def on_mount(self):
        self.chat_num = 1
        self.push_screen("Main")
        if cn == None:
            self.push_screen("cc")


if __name__ == "__main__":
    Main().run()

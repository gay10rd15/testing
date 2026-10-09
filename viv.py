import os
import re
import subprocess
import sys
import webbrowser

import pyttsx3
import speech_recognition as sr

# Check for mac_imessage availability
try:
    import mac_imessage

    IMESSAGE_AVAILABLE = True
except ImportError:
    print("Warning: mac_imessage not found. iMessage features will be disabled.")
    IMESSAGE_AVAILABLE = False

# --- Configuration ---
VOICE_ID = "com.apple.speech.synthesis.voice.Alex"
WAKE_WORDS = ["hello", "hello viv"]
EXIT_COMMANDS = ["exit", "quit", "stop"]

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "contacts.txt")


def load_contacts():
    contacts = {}
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and ": " in line:
                    name, number = line.split(": ", 1)
                    contacts[name.strip()] = number.strip()
    return contacts


def get_phone_number(target):
    if re.search(r"\d", target):
        return "".join(filter(str.isdigit, target))
    if target in contacts:
        return "".join(filter(str.isdigit, contacts[target]))
    print(f"Contact '{target}' not found.")
    sys.exit(1)


contacts = load_contacts()

# --- Initialization ---
recognizer = sr.Recognizer()
engine = pyttsx3.init(driverName="nsss")
engine.setProperty("rate", 190)
voices = engine.getProperty("voices")

voice_set = False
# pyrefly: ignore [not-iterable]
for voice in voices:
    if VOICE_ID in voice.id:
        engine.setProperty("voice", voice.id)
        voice_set = True
        break
if not voice_set:
    print(f"Voice {VOICE_ID} not found, using default.")


def sayt(text):
    """Convert text to speech."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen_command(timeout=None, phrase_time_limit=None):
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
            # pyrefly: ignore [missing-attribute]
            text = recognizer.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
    except OSError:
        print("Error: No microphone detected.")
        return None
    except sr.WaitTimeoutError:
        print("Listening timed out.")
        return None
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"API Error: {e}")
        return None


def send_message_via_applescript(message, recipient):
    """
    Fallback method using AppleScript to send iMessage if library fails.
    Note: Requires Accessibility permissions for Terminal/Python.
    """
    # Escape quotes in message to prevent script injection
    safe_message = message.replace('"', '\\"')
    script = f'''
    tell application "Messages"
        set target_buddy to "{recipient}"
        send "{safe_message}" to buddy target_buddy of (service 1 whose service type is iMessage)
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def send_message_flow():
    """Handles the multi-step process of sending a message."""
    if not IMESSAGE_AVAILABLE:
        sayt("iMessage library not found. Using AppleScript fallback if possible.")

    message_content = listen_command()

    if not message_content:
        sayt("I didn't catch that. Cancelling message.")
        return

    recipient = listen_command()

    if not recipient:
        sayt("No recipient heard. Cancelling.")
        return

    recipient = get_phone_number(recipient)

    sayt(f"Sending to {recipient}.")

    success = False
    # Try library first
    if IMESSAGE_AVAILABLE:
        mac_imessage.send(
            message=message_content, phone_number=recipient, medium="imessage"
        )
        success = True
    if not success:
        print("Attempting AppleScript fallback...")
        if send_message_via_applescript(message_content, recipient):
            success = True

    if success:
        sayt("Message sent successfully!")
    else:
        sayt("Failed to send message. Check permissions or recipient details.")


def search():

    wts = listen_command()

    if not wts:
        sayt("nothing to search for")
    else:
        # 1. Replace spaces with '+'
        # 2. Construct the full URL string
        search_url = (
            f"https://search.brave.com/search?q={wts.replace(' ', '+')}&source=web"
        )

        # 3. Pass the single URL string to webbrowser.open
        webbrowser.open(search_url)


# --- Main Loop ---
if __name__ == "__main__":
    while True:
        text = listen_command()

        if not text:
            continue

        # Wake Word / Greeting
        if any(word in text for word in WAKE_WORDS):
            sayt("Hello, Parker")

        # Exit Command
        elif any(cmd in text for cmd in EXIT_COMMANDS):
            sayt("Shutting down.")
            break

        # Open Website
        elif text.startswith("open"):
            app = listen_command()
            if app == None:
                sayt("no app detected")
            else:
                app_path = "/Applications/" + app + ".app"
                subprocess.run(["open", app_path], check=False)

        # Send Message
        elif "send message" in text or "send a message" in text:
            send_message_flow()

        elif any(
            phrase in text for phrase in ["search", "search the web", "search for"]
        ):
            search()
        else:
            pass

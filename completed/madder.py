# add metadata to audio files

import crossfiledialog
import music_tag
import questionary

af = crossfiledialog.open_file(filter=["*.mp3", "*.ogg", "*.wav", "*.flac"])

faf = music_tag.load_file(af)

# pyrefly: ignore [unsupported-operation]
print(f"the current artist is {faf['artist']}")
# pyrefly: ignore [unsupported-operation]
print(f"the current title is {faf['title']}")
# pyrefly: ignore [unsupported-operation]
print(f"the current title is {faf['album']}")

wtd = questionary.checkbox(
    "what do you want to do?",
    choices=[
        "add artist",
        "add title",
        "add album",
        "reset track number",
        "add cover image",
    ],
).ask()

if "add artist" in wtd:
    artist = input("what is the artists name \n> ")
    # pyrefly: ignore [unsupported-operation]
    faf["artist"] = artist

if "add title" in wtd:
    title = input("what is the title of the song\n> ")
    # pyrefly: ignore [unsupported-operation]
    faf["title"] = title
if "add album" in wtd:
    album = input("what is the songs album?\n> ")
    # pyrefly: ignore [unsupported-operation]
    faf["album"] = album

if "reset track number" in wtd:
    # pyrefly: ignore [missing-attribute]
    faf.raw["tracknumber"] = ""

if "add cover image" in wtd:
    image = crossfiledialog.open_file(filter=["*.png", "*.jpeg", "*.svg", "*.heic"])
    with open(image, "rb") as img_data:
        # pyrefly: ignore [unsupported-operation]
        faf["artwork"] = img_data.read()

# pyrefly: ignore [missing-attribute]
faf.save()

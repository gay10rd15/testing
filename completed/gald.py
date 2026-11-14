import os
import re
import sys
from pathlib import Path

# Setup file path
root_dir = Path(sys.executable).anchor
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = Path(script_dir) / "roots.txt"
file_path.parent.mkdir(parents=True, exist_ok=True)

# you will have to edit the roots.txt file manually

try:
    with open(file_path, "r") as f:
        roots = [line.strip() for line in f if line.strip()]
        f.flush()
except FileNotFoundError:
    print("file not found")
    print("creating")
    print("add the roots now")
    with open(file_path, "w") as f:
        f.write("# roots file for gald.py")
        f.flush()
    sys.exit()
# FILTER: filter out any words
filter_words = {
    "the",
    "a",
    "is",
    "in",
    "it",
    "to",
    "and",
    "are",
    "of",
    "for",
    "on",
    "with",
    "as",
    "by",
    "that",
    "this",
}


print("Enter a sentence to search for roots")
ui = input("> ")
found_any = False
for word in ui.split():
    clean_word = re.sub(r"[.,!?]", "", word)
    if clean_word.lower() in filter_words:
        continue
    for root_entry in roots:
        root_key = root_entry.split(maxsplit=1)[0]
        if re.search(root_key, clean_word, re.IGNORECASE):
            print(f"Found match in {word} : {root_entry}")
            found_any = True
if not found_any:
    print("no matches found in: " + ui)

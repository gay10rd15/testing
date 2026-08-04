import questionary, os
from pathlib import Path

print("welcome to the dnd character creator!")
fpath = Path(__file__).parent.resolve() / "character.txt"
print(fpath)

def check(variable):
    if variable == None:
        quit("you cannot have nothing as a part of your character?")

name = questionary.text("whats you character's name").ask()

cclass = questionary.select(
    "select a class",
    choices=[
        "barbarian",
        "bard",
        "cleric",
        "druid",
        "fighter",
        "monk",
        "paladin",
        "ranger",
        "rogue",
        "sorcerer",
        "warlock",
        "wizard"
    ]
).ask()

check(cclass)


while True:
    level = int(questionary.text("what level are you?").ask())
    if level < 1:
        print("level cannot be lower than 1")
    elif level > 20:
        print("level cannot be over 20")
    else:
        break

with open(fpath, 'w') as f:
    f.write("character name: " + name)
    f.write("\nclass: " + cclass)
    f.write("\nlevel: " + str(level))





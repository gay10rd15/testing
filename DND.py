import os
from pathlib import Path

import questionary

print("welcome to the dnd character creator!")
fpath = Path(__file__).parent.resolve() / "character.txt"
print(fpath)


def check(variable):
    if variable == None:
        quit("you cannot have nothing as a part of your character?")


name = questionary.text("whats you character's name").ask()

# Choose class

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
        "wizard",
    ],
).ask()


check(cclass)

# Choose level

while True:
    level = int(questionary.text("what level are you?").ask())
    if level == "":
        level = 1
    if level < 1:
        print("level cannot be lower than 1")
    elif level > 20:
        print("level cannot be over 20")
    else:
        break

# Pick subclass
# I will add more subclasses from the other books later

if cclass == "barbarian":
    subclass = questionary.select(
        "pick a barbarian subclass",
        choices=["berserker", "wild heart", "world tree", "zealot"],
    ).ask()
if cclass == "bard":
    subclass = questionary.select(
        "pick a bard subclass",
        choices=[
            "school of dance",
            "school of glamour",
            "school of lore",
            "school of valor",
        ],
    ).ask()

if cclass == "cleric":
    subclass = questionary.select(
        "pick a cleric subclass",
        choices=[
            "Death domain",
            "Life domain",
            "Light domain",
            "Nature domain",
            "Tempest domain",
            "Trickery domain",
            "war domain",
        ],
    ).ask()

if cclass == "druid":
    subclass = questionary.select(
        "pick a druid subclass",
        choices=[
            "Circle of the land",
            "Circle of the Moon",
            "Circle of the sea",
            "Circle of the stars",
        ],
    ).ask()

if cclass == "fighter":
    subclass = questionary.select(
        "pick a fighter subclass",
        choices=["Battle master", "Champion", "Eldritch knight", "Psi warrior"],
    ).ask()

if cclass == "monk":
    subclass = questionary.select(
        "select a monk subclass",
        choices=[
            "Warrior of the elements",
            "Warrior of mercy",
            "Warrior of the open hand",
            "Warrior of shadow",
        ],
    )

if cclass == "paladin":
    subclass = questionary.select("select a paladin subclass", choices=[])

# pyrefly: ignore [unbound-name]
check(subclass)

with open(fpath, "w") as f:
    f.write("character name: " + name)
    f.write("\nclass: " + cclass)
    f.write("\nlevel: " + str(level))
    f.write("\nsubclass: " + str(subclass))

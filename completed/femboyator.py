import random
import re

txt = input("enter a sentence\n> ")
rep = [
    " ~uwu~ ",
    " XD ",
    " (˶>⩊<˶) ",
    " (˶  >   ₃  < ˶) ",
    " (,,>﹏<,,) ",
    " ",
    " ",
    " ",
    " ",
]

bruh1 = ["bro", "bruh", "dude"]
bruh2 = ["senpai", "master"]

txt = re.sub(r" ", lambda match: random.choice(rep), txt)

final = txt.split()

for i, word in enumerate(final):
    if word.lower() in bruh1:
        final[i] = random.choice(bruh2)

txt = " ".join(final)
print(txt)

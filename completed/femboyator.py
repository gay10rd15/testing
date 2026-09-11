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

bruhs = ["bruh", "bro", "dude"]
bruhr = ["senpai", "master"]

for word in txt.split():
    if word in bruhs:
        txt = re.sub(word, random.choice(bruhr), txt)


end = re.sub(r" ", random.choice(rep), txt)

print(end)

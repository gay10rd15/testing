import re
import random

txt = input("enter a sentence\n> ")
rep = [" ~uwu~ ", " XD ", " (˶>⩊<˶) ", " (˶  >   ₃  < ˶) ", " (,,>﹏<,,) ", " ", " ", " ", " "]

def replace_space(match):
    return random.choice(rep)

end = re.sub(r" ", replace_space, txt)

print(end)   

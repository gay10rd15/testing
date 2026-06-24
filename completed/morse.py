stm = {
    "a": "•-",
    "b": "-•••",
    "c": "-•-•",
    "d": "-•••",
    "e": "•",
    "f": "••-•",
    "g": "--•",
    "h": "••••",
    "i": "••",
    "j": "•---",
    "k": "-•-",
    "l": "•-••",
    "m": "--",
    "n": "-•",
    "o": "---",
    "p": "•--•",
    "q": "--•-",
    "r": "•-•",
    "s": "•••",
    "t": "-",
    "u": "••-",
    "v": "•••-",
    "w": "•--",
    "x": "-••-",
    "y": "-•--",
    "z": "--••"
}

ui = input("enter a string to turn it to morse code!\n> ")

translated = []
for char in ui:
    if char in stm:
        translated.append(stm[char])
    elif char == ' ':
        translated.append('  ')
    else:
        translated.append("?")

print(*translated)
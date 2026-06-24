import random as r
import questionary

def f(flower):
    a = r.randint(1, 10)
    return a, f"{flower}: {a}"

a, roses = f("roses")
b, sunflowers = f("sunflowers")
c, orchids = f("orchids")
d, lillies = f("lillies")
e, tulips = f("tulips")
f, peonies = f("peonies")

flower_stock = {
    "roses": a,
    "sunflowers": b,
    "orchids": c,
    "lillies": d,
    "tulips": e,
    "peonies": f
}

flowers = [roses, sunflowers, orchids, lillies, tulips, peonies]

choices = questionary.select(
    "What would you like to do?",
    choices=["get hours", "get inventory", "buy flowers", "quit"]
).ask()

if choices == "get hours":
    print("We are open from 10-5 Monday through Friday.")
elif choices == "quit":
    print("Now quitting...")
    quit()
elif choices == "get inventory":
    print(*flowers, sep='\n')
    print("This is all we have in stock for now.\nCome back later for different flowers.")
elif choices == "buy flowers":
    cart = {flower: 0 for flower in flower_stock}

    while True:
        available_choices = [
            f"{name} (available: {flower_stock[name] - cart[name]})"
            for name in flower_stock if cart[name] < flower_stock[name]
        ]

        if not available_choices:
            print("You've bought all available flowers!")
            break

        choice = questionary.select(
            "Select a flower to add to your cart:",
            choices=available_choices + ["Done selecting"]
        ).ask()

        if choice == "Done selecting":
            break

        selected_flower = choice.split(" (")[0]

        if cart[selected_flower] < flower_stock[selected_flower]:
            cart[selected_flower] += 1
            print(f"Added {selected_flower}. (Count: {cart[selected_flower]})")
        else:
            print(f"No more {selected_flower} available!")

    print("\nYour final order:")
    for flower, count in cart.items():
        if count > 0:
            print(f"{flower}: {count}")   
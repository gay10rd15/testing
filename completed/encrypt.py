import random
import sys
import time


def shuffle_under_seed(ls, seed):
    items = list(ls)
    random.seed(seed)
    indices = list(range(len(items)))
    random.shuffle(indices)
    shuffled = [items[i] for i in indices]
    return "".join(shuffled), indices


def unshuffle_list(shuffled_ls, indices):
    original = [""] * len(shuffled_ls)
    for i, original_index in enumerate(indices):
        original[original_index] = shuffled_ls[i]
    return "".join(original)


x = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()"
y = "zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA1234567890"
mt = str.maketrans(x, y)


def cl(n=1):
    for _ in range(n):
        sys.stdout.write("\x1b[1A\x1b[2K")
        sys.stdout.flush()


while True:
    choice = input("encode or decode? (q to quit): ").lower()
    if choice == "q":
        cl(1)
        break

    if choice in ["encode", "e"]:
        key = input("Input the key: ")
        text = input("what do you want to encode: ")
        translated = text.translate(mt)
        result, indices = shuffle_under_seed(translated, key)
        print(f"Encoded text: {result}")

    elif choice in ["decode", "d"]:
        key = input("Input the key: ")
        text = input("what do you want to decode: ")
        n = len(text)
        indices = list(range(n))
        random.seed(key)
        random.shuffle(indices)
        unshuffled = unshuffle_list(text, indices)
        result = unshuffled.translate(mt)
        print(f"Decoded text: {result}")

    else:
        print("Invalid choice.")
        time.sleep(1)
        cl(2)
        continue

    input("\nPress Enter to continue...")
    cl(6)

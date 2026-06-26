import time
import os
import sys
import random

def shuffle_under_seed(ls, seed):
    # Convert string to list
    items = list(ls)
    # Set seed for reproducibility
    random.seed(seed)
    # Shuffle and track indices
    indices = list(range(len(items)))
    random.shuffle(indices)  # This defines the shuffle map
    # Apply shuffle
    shuffled = [items[i] for i in indices]
    return "".join(shuffled), indices

def unshuffle_list(shuffled_ls, indices):
    # Reverse the shuffle using recorded indices
    original = [''] * len(shuffled_ls)
    for i, original_index in enumerate(indices):
        original[original_index] = shuffled_ls[i]
    return "".join(original)

# Atbash-style translation maps
x = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()'
y = 'zyxwvutsrqponmlkjihgfedcbaZYXWVUTSRQPONMLKJIHGFEDCBA1234567890'
mt = str.maketrans(x, y)

def cl(n=1):
    for _ in range(n):
        sys.stdout.write('\x1b[1A\x1b[2K')  # Move up and clear line
        sys.stdout.flush()

while True:
    choice = input("encode or decode? (q to quit): ").lower()
    if choice == 'q':
        cl(1)
        break

    if choice in ['encode', 'e']:
        key = input("Input the key: ")
        text = input("what do you want to encode: ")
        translated = text.translate(mt)
        result, indices = shuffle_under_seed(translated, key)
        # Store indices for decoding (e.g., save alongside ciphertext)
        print(f"Encoded text: {result}")
        # For real use, save `indices` or derive from seed reliably
        # ⚠️ Note: We can't reconstruct indices without saving or re-running shuffle

    elif choice in ['decode', 'd']:
        key = input("Input the key: ")
        text = input("what do you want to decode: ")
        # Recreate the same shuffle indices using the seed
        n = len(text)
        indices = list(range(n))
        random.seed(key)
        random.shuffle(indices)  # Same shuffle order as encoding
        # Now unshuffle using these indices
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

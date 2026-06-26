import random, argparse

def print_card(rank, suit):
    """
    Prints an ASCII representation of a single playing card.

    Args:
        rank (str): The rank of the card ('2'-'10', 'J', 'Q', 'K', 'A').
        suit (str): The suit of the card ('♠', '♥', '♦', '♣').
    """
    top = "┌─────────┐"
    bottom = "└─────────┘"
    side = "│         │"

    if rank == "10":  # Ten is the only rank with two digits
        rank_right = rank
        rank_left = rank
    else:
        rank_right = rank + " "
        rank_left = " " + rank

    suit_line = f"│    {suit}    │"
    rank_line_left = f"│{rank_left}       │"
    rank_line_right = f"│       {rank_right}│"

    print(top)
    print(rank_line_left)
    print(side)
    print(suit_line)
    print(side)
    print(rank_line_right)
    print(bottom)

ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ['\u2660', '\u2665', '\u2666', '\u2663']

def main():
    suit = random.choice(suits)
    rank = random.choice(ranks)
    print_card(rank, suit)
    print()  # Add a space between cards


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("number", help="number of cards drawn", default=1)
    args = parser.parse_args()
    for num in range(int(args.number)):
        main()
    

import random
import questionary
import os

MONEY_FILE = "money.txt"
CARDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def get_hand_value(hand):
    """Calculate hand value, handling Aces as 1 or 11."""
    value = sum(hand)
    aces = hand.count(1)
    while aces > 0 and value + 10 <= 21:
        value += 10
        aces -= 1
    return value

def draw_card():
    return random.choice(CARDS)

def save_money(amount):
    with open(MONEY_FILE, "w") as f:
        f.write(str(amount))

def load_money():
    if not os.path.exists(MONEY_FILE):
        save_money(100)
        return 100
    try:
        with open(MONEY_FILE, "r") as f:
            return int(f.read().strip())
    except (ValueError, FileNotFoundError):
        save_money(100)
        return 100

print("Welcome to Blackjack!")

player_money = load_money()

if player_money <= 0:
    print("You're out of money! Here's $100 to start again.")
    player_money = 100
    save_money(player_money)

while True:
    if player_money <= 0:
        print("Game Over! You ran out of money.")
        break

    print(f"\nYou have ${player_money}")

    while True:
        try:
            bet = int(input("How much do you want to bet? > "))
            if 0 < bet <= player_money:
                break
            else:
                print("Invalid bet amount. You don't have enough money.")
        except ValueError:
            print("Please enter a number.")

    # Deduct bet
    player_money -= bet
    dealer_bet = random.choice([5, 5, 5, 5, 5, 10, 10, 10, 10, 15, 15, 15, 20, 20, 25])
    pot = bet + dealer_bet
    print(f"The dealer bets ${dealer_bet}. Total pot: ${pot}")

    # Deal initial cards
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card(), draw_card()]
    
    player_total = get_hand_value(player_hand)
    print(f"You have: {player_hand} (Total: {player_total})")
    print(f"Dealer shows: {dealer_hand[0]} and [Hidden]")

    if player_total == 21:
        print("Blackjack!")
        if get_hand_value(dealer_hand) == 21:
            print("Dealer also has Blackjack. It's a tie!")
            player_money += bet  # Return bet
        else:
            print("You win!")
            player_money += int(pot * 1.5) 
        save_money(player_money)
        # Ask to play again
        if questionary.select("Play again?", choices=["yes", "no"]).ask() == "no":
            break
        continue

    while True:
        if player_total > 21:
            print("You busted!")
            break
        
        choice = questionary.select("Hit or Stay?", choices=["hit", "stay"]).ask()
        
        if choice == "hit":
            new_card = draw_card()
            player_hand.append(new_card)
            player_total = get_hand_value(player_hand)
            print(f"You drew: {new_card}. Hand: {player_hand} (Total: {player_total})")
        else:
            print(f"You stay with {player_total}")
            break

    if player_total > 21:
        print("You lose this round.")
        save_money(player_money)
    else:
        dealer_total = get_hand_value(dealer_hand)
        print(f"\nDealer reveals: {dealer_hand} (Total: {dealer_total})")
        
        while dealer_total < 17:
            new_card = draw_card()
            dealer_hand.append(new_card)
            dealer_total = get_hand_value(dealer_hand)
            print(f"Dealer hits: {new_card}. Hand: {dealer_hand} (Total: {dealer_total})")

        if dealer_total > 21:
            print("Dealer busted! You win!")
            player_money += pot
        elif player_total > dealer_total:
            print("You win!")
            player_money += pot * 2
        elif player_total < dealer_total:
            print("Dealer wins.")
        else:
            print("It's a tie (Push).")
            player_money += bet 

    save_money(player_money)

    if questionary.select("Play again?", choices=["yes", "no"]).ask() == "no":
        print(f"Goodbye! You leave with ${player_money}")
        break   
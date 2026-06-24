import random
import time as T
import os
import inspect
def round_to_5(x):
    return 5 * round(x / 5)
cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
dm = [5, 5, 5, 5, 5, 10, 10, 10, 10, 15, 15, 15, 20, 20, 25]
stack = inspect.stack()
try:
    caller_file = inspect.stack()[1].filename
except IndexError:
    caller_file = __file__ 
path = os.path.dirname(os.path.abspath(caller_file)) + "money.txt"

try:
    with open("money.txt", "r") as f:
        ym = int(f.read().strip())
except FileNotFoundError:
    ym = 100  # Default starting money if file doesn't exist
    with open("money.txt", "w") as f:
        f.write(str(ym))
except Exception as e:
    print(e)
while True:
    if ym <= 0:
        print("You are out of money!")
        print("you get 100$ more to play with")
        ym += 100  # Reset money to 100
        open("money.txt", "w").write(str(ym))
    print("\n--- New Game ---")
    db = random.choice(dm)
    print(f"The dealer bets {db}")
    
    while True:
        T.sleep(1)
        print(f"\nYou have {ym}$")
        T.sleep(1)
        print("How much do you want to bet?")
        T.sleep(0.25)
        print("or enter q to quit")
        T.sleep(0.25)
        pb_input = input(">")
        
        if pb_input == "q":
            quit()
            
        # 1. Validate input is a number
        if not pb_input.isdigit():
            print("Invalid input. Please enter a number.")
            continue
            
        pb = int(pb_input)
        pb = round_to_5(pb)
        print(f"you bet {pb}")
        T.sleep(.5)
        # 2. CHECK IF PLAYER HAS ENOUGH MONEY
        if pb > ym:
            print(f"You cannot bet {pb}$. You only have {ym}$.")
            continue # Prompts for bet again
        elif pb <= 0:
            print("Bet must be positive.")
            continue
        else:
            ym -= pb # Deduct the bet securely
            break
            
    pot = pb + db
    dh = [random.choice(cards), random.choice(cards)]
    ph = [random.choice(cards), random.choice(cards)]
    print(f"the pot is now {pot}")
    # Hidden dealer card visible as first card (dh[0])
    print(f"The dealer's visible card: {dh[0]}")
    T.sleep(1)
    # 3. Player's turn
    while True:
        # Summing the list using sum()
        ph_total = sum(ph)
        print(f"your hand: {ph} (total: {ph_total})")
        T.sleep(1)
        if ph_total == 21:
            print("Blackjack! You win!")
            break
        elif ph_total > 21:
            print("You busted!")
            break
        
        print("do you want to hit or stay?")
        ui = input("> ").lower()
        if ui == "hit" or ui == "h":
            ph.append(random.choice(cards))
        elif ui == "stay" or ui == "s":
            print(f"you stand with {ph_total}")
            break
    
    # 4. Dealer's Turn Logic (if player didn't bust)
    if sum(ph) <= 21:
        while True:
            dh_total = sum(dh)
            print(f"Dealer's hand: {dh} (total: {dh_total})")
            
            if dh_total < 17:
                # Dealer must hit
                nc = random.choice(cards)
                dh.append(nc)
                print(f"the dealer hit and drew {nc}")
                T.sleep(2)
            elif 17 <= dh_total <= 21:
                # Dealer must stand
                print(f"The dealer stands with: {dh_total}")
                break
            else:
                # Dealer busted
                T.sleep(2)
                print("The dealer busted!")
                break
        
        # Who will win
        dh_final = sum(dh)
        ph_final = sum(ph)
            
        if dh_final > 21 or ph_final > dh_final:
            T.sleep(2)
            print("you win! good job!"); T.sleep(1.5) 
            ym += pot * 2
        elif ph_final < dh_final:
            print("you lose")
        else:
            print("it's a tie")
            ym += pb
    open("money.txt", "w").write(str(ym)) # Save money after each game       
    print("----------------")
    
    # Optional: loop to play again
    T.sleep(1)
    play_again = input("Play again? (y/n) > ").lower()
    if play_again != 'n':
        continue
    else:
        break
    print("----------------")
    
   
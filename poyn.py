import os

def main():
    # --- Setup ---
    try:
        nop = int(input("Enter number of players: "))
        if nop < 2:
            print("You need at least 2 players.")
            return
    except ValueError:
        print("Invalid number.")
        return

    player_names = []
    player_scores = [0] * nop  # Cumulative scores

    for i in range(nop):
        pn = input(f"Enter name for player {i + 1}: ").strip()
        player_names.append(pn)

    try:
        num_of_rounds = int(input("Enter number of rounds: "))
    except ValueError:
        print("Invalid number of rounds.")
        return

    # Lists to store history for the final report
    all_round_bets = []
    all_round_wins = []
    all_round_scores = []

    # --- Game Loop ---
    for rnd in range(num_of_rounds):
        current_round = rnd + 1
        print(f"\n--- Round Number {current_round} (Cards: {current_round}) ---")
        
        round_bets = []
        round_wins = []
        round_points = []

        # 1. Get Bets
        for i in range(nop):
            cpn = player_names[i]
            while True:
                try:
                    raw_input = input(f"What does {cpn} think they will win? ").strip()
                    pb = int(raw_input)
                    
                    # Dealer condition: Total bids cannot equal the number of cards
                    if i == nop - 1: # If this is the last player (dealer)
                        total_previous_bets = sum(round_bets)
                        if total_previous_bets + pb == current_round:
                            print(f"Invalid bid! Total bids ({total_previous_bets + pb}) cannot equal the number of cards ({current_round}).")
                            continue
                    
                    round_bets.append(pb)
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")

        # 2. Get Actual Wins
        for i in range(nop):
            cpn = player_names[i]
            while True:
                try:
                    pw = int(input(f"What did {cpn} actually win? ").strip())
                    if pw < 0:
                        print("Wins cannot be negative.")
                        continue
                    round_wins.append(pw)
                    break
                except ValueError:
                    print("Enter a valid number.")

        # 3. Calculate Scores
        print("\nRound Results:")
        for i in range(nop):
            bet = round_bets[i]
            win = round_wins[i]
            points = 0

            if bet == win:
                points = 10 * win  # Standard rule: 10 for exact + 1 per trick
                print(f"{player_names[i]}: Bet {bet} | Won {win} -> +{points} points")
            elif bet < win:
                points = win # Usually just the number of tricks won if over-bid (rules vary)
                print(f"{player_names[i]}: Bet {bet} | Won {win} -> +{points} points (Over)")
            else:
                # Bet > Win: Usually 0 points, or sometimes negative. Here we do 0.
                points = (bet - win) * -10
                print(f"{player_names[i]}: Bet {bet} | Won {win} -> {(bet - win) * -10} points (Under)")

            player_scores[i] += points
            round_points.append(points)

        # Store history for final report
        all_round_bets.append(round_bets)
        all_round_wins.append(round_wins)
        all_round_scores.append(round_points)

        # Show current standings
        print("\n--- Current Standings ---")
        for i in range(nop):
            print(f"{player_names[i]}: {player_scores[i]} points")

    # --- Final Output to File ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    final_path = os.path.join(script_dir, "output.txt")

    with open(final_path, "w") as f:
        f.write("FINAL SCOREBOARD\n")
        f.write("=" * 40 + "\n\n")
        
        # Write Final Totals
        f.write(f"{'Player':<20} | {'Total Score':>10}\n")
        f.write("-" * 35 + "\n")
        for i in range(nop):
            f.write(f"{player_names[i]:<20} | {player_scores[i]:>10}\n")
        
        f.write("\n\nDETAILED ROUND HISTORY\n")
        f.write("=" * 40 + "\n")

        # Write Round Details
        for r in range(num_of_rounds):
            f.write(f"\nRound {r+1} (Cards: {r+1})\n")
            f.write(f"{'Player':<15} | {'Bet':>5} | {'Won':>5} | {'Pts':>5}\n")
            f.write("-" * 35 + "\n")
            for i in range(nop):
                b = all_round_bets[r][i]
                w = all_round_wins[r][i]
                p = all_round_scores[r][i]
                f.write(f"{player_names[i]:<15} | {b:>5} | {w:>5} | {p:>5}\n")

    print(f"\nGame Over! Results saved to {final_path}")

if __name__ == "__main__":
    main()   


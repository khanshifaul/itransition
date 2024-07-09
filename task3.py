import hmac
import random
import secrets
import sys
from collections import OrderedDict

from tabulate import tabulate


def help():
    """Prints the game rules to the console."""
    print(
        """Welcome to the Generalized Rock-Paper-Scissors game!

Here are the rules:

* You can choose a move by its index (number) or its name.
* Available moves are displayed at the beginning of the game.
* 0 - Exit the game
* ? - Print this help message

**Game Rules:**

* Each move competes against half of the following moves in a circular order.
* The goal is to choose a move that beats the computer's move.
* If you choose the same move as the computer, it's a tie!
"""
    )
    generate_outcomes_table()
    exit()


def exit():
    sys.exit(0)


def generate_outcomes_table():
    moves = ["Rock", "Paper", "Scissors", "Lizard", "Spock"]
    outcomes = {
        "Rock": {
            "Rock": "Tie",
            "Paper": "Lose",
            "Scissors": "Win",
            "Lizard": "Win",
            "Spock": "Lose",
        },
        "Paper": {
            "Rock": "Win",
            "Paper": "Tie",
            "Scissors": "Lose",
            "Lizard": "Lose",
            "Spock": "Win",
        },
        "Scissors": {
            "Rock": "Lose",
            "Paper": "Win",
            "Scissors": "Tie",
            "Lizard": "Win",
            "Spock": "Lose",
        },
        "Lizard": {
            "Rock": "Lose",
            "Paper": "Win",
            "Scissors": "Lose",
            "Lizard": "Tie",
            "Spock": "Win",
        },
        "Spock": {
            "Rock": "Win",
            "Paper": "Lose",
            "Scissors": "Win",
            "Lizard": "Lose",
            "Spock": "Tie",
        },
    }

    table = []
    for move in moves:
        row = [move]
        for opponent in moves:
            row.append(outcomes[move][opponent])
        table.append(row)

    headers = ["⬇️ You / Computer ➡️"] + moves
    print("Move Outcomes Table:")
    print(tabulate(table, headers, tablefmt="grid"))


def generate_secret_key():
    secret_key = secrets.token_bytes(32).hex()
    return secret_key


def compute_hmac(secret_key, choice):
    secret_key_bytes = bytes.fromhex(secret_key)
    return hmac.new(secret_key_bytes, choice.encode(), digestmod="sha256").hexdigest()


def available_moves(moves):
    """Print available moves to the console."""
    print("Available moves:")
    for i, move in enumerate(moves, start=1):
        print(f"{i} - {move}")
    print("0 - Exit")
    print("? - Help")


def computer_move(moves):
    """Generate a random move for the computer."""
    return random.choice(moves)


def user_move(moves):
    """Prompt user for move input and validate."""
    while True:
        user_choice = input("Enter your move: ")

        if user_choice == "?":
            help()
        elif user_choice.isdigit():
            choice_index = int(user_choice)
            if choice_index == 0:
                print("Exiting the game...")
                exit()
            elif 1 <= choice_index <= len(moves):
                return moves[choice_index - 1]
        elif user_choice in moves:
            return user_choice

        print("Invalid input. Please choose from available options.")


def determine_winner(user_move, computer_move, moves):
    """Determine and print the winner of the game."""
    index_user = moves.index(user_move)
    index_computer = moves.index(computer_move)
    difference = (index_user - index_computer) % len(moves)

    if index_user == index_computer:
        print("It's a tie!")
    elif difference == (len(moves) // 2):
        print("You Win!")
    else:
        print("Computer Wins!")


def get_winner(user_move, computer_move):
    """Determine and print the winner of the game."""
    print(f"Your Move: {user_move}")
    print(f"Computer Move: {computer_move}")

    # Define move outcomes in a circular order
    outcomes = {
        "rock": {
            "rock": "tie",
            "paper": "lose",
            "scissors": "win",
            "lizard": "win",
            "spock": "lose",
        },
        "paper": {
            "rock": "win",
            "paper": "tie",
            "scissors": "lose",
            "lizard": "lose",
            "spock": "win",
        },
        "scissors": {
            "rock": "lose",
            "paper": "win",
            "scissors": "tie",
            "lizard": "win",
            "spock": "lose",
        },
        "lizard": {
            "rock": "lose",
            "paper": "win",
            "scissors": "lose",
            "lizard": "tie",
            "spock": "win",
        },
        "spock": {
            "rock": "win",
            "paper": "lose",
            "scissors": "win",
            "lizard": "lose",
            "spock": "tie",
        },
    }

    outcome = outcomes[user_move][computer_move]

    if outcome == "tie":
        print("It's a tie!")
    elif outcome == "win":
        print("You Win!")
    else:
        print("Computer Wins!")


def main():
    # Validate command line arguments
    moves = sys.argv[1:]
    moves = list(OrderedDict.fromkeys(moves))

    if len(moves) < 3 or len(moves) % 2 == 0:
        print("Invalid number of moves provided.")
        print("Please provide an odd number of moves (≥ 3) as command line arguments.")
        print("Example: python task3.py rock paper scissors lizard spock")
        sys.exit(1)

    secret_key = generate_secret_key()

    # Generate computer's move and compute HMAC
    computer_move_choice = computer_move(moves)
    computer_hmac = compute_hmac(secret_key, computer_move_choice)
    print(f"Computer's HMAC: {computer_hmac}")
    available_moves(moves)
    user_move_choice = user_move(moves)
    print(f"Your Move: {user_move_choice}")
    print(f"Computer Move: {computer_move_choice}")

    # Determine winner
    # get_winner(user_move_choice, computer_move_choice)
    determine_winner(user_move_choice, computer_move_choice, moves)
    print(f"secret_key: {secret_key}")


if __name__ == "__main__":
    main()


# python task3.py rock paper scissors
# ["0"]
# python task3.py rock paper scissors
# ["?"]
# python task3.py rock paper scissors
# ["1"]
# python task3.py rock paper scissors
# ["5"]
# python task3.py rock paper
# ["1"]
# python task3.py rock paper paper scissors
# ["2"]
# python task3.py rock paper scissors lizard spock
# ["3"]
# python task3.py rock paper scissors lizard spock dragon wizard
# ["4"]
# python task3.py alpha beta gamma
# ["1"]
# python task3.py 1 2 3 4 5
# ["2"]

import hmac
import random
import secrets
import sys
from collections import OrderedDict

from tabulate import tabulate


def help(moves):
    """Prints the game rules to the console."""
    print(
        """Welcome to the Rock-Paper-Scissors game!

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
    generate_outcomes_table(moves)
    exit()


def exit():
    sys.exit(0)


def generate_outcomes_table(moves):
    outcomes = {}
    num_moves = len(moves)
    half_moves = num_moves // 2

    for i, move in enumerate(moves):
        outcomes[move] = {}
        for j, opponent in enumerate(moves):
            if i == j:
                outcomes[move][opponent] = "Tie"
            elif (j - i) % num_moves <= half_moves:
                outcomes[move][opponent] = "Lose"
            else:
                outcomes[move][opponent] = "Win"

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
            help(moves)
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
    determine_winner(user_move_choice, computer_move_choice, moves)
    print(f"secret_key: {secret_key}")


if __name__ == "__main__":
    main()

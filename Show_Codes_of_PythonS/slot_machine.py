import random
from typing import Mapping

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "7": 2,
    "BAR": 4,
    "CHERRY": 6,
    "LEMON": 8,
    "ORANGE": 10
}

symbol_value = {
    "7": 10,
    "BAR": 5,
    "CHERRY": 2,
    "LEMON": 1,
    "ORANGE": 1
}

def check_winnings(columns: list[list[str]], lines: int, bet: float, values: Mapping[str, float]) -> tuple[float, list[int]]:
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines
    return winnings, winning_lines


def get_slot_machine_spin(rows: int, cols: int, symbols: dict[str, int]) -> list[list[str]]:
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns


def print_slot_machine(columns: list[list[str]]):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns)-1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()


def deposit():
    while True:
        try:
            amount = float(input("What would you like to deposit? $"))
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        except ValueError:
            print("Please enter a valid number.")

    return amount


def get_number_of_lines():
    while True:
        try:
            lines = int(input(
                "Enter the number of lines to bet on (1-" + str(MAX_LINES) + ")? "))
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        except ValueError:
            print("Please enter a number.")

    return lines


def get_bet():
    while True:
        try:
            amount = float(input("What would you like to bet on each line? $ "))
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        except ValueError:
            print("Please enter a valid number.")

    return amount


def spin(balance: float) -> float:
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet*lines


        if total_bet > balance:
            print(
                f"You do not have enough money to bet that amount, your current balance is: ${balance:.2f}.")

        else:
            break

    print(
        f"You are betting ${bet:.2f} on {lines} lines. Total bet is equal to: ${total_bet:.2f}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings:.2f}.")
    if winning_lines:
        print(f"You won on lines: {', '.join(map(str, winning_lines))}")
    return winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance:.2f}")
        answer = input("Press enter to play (q to quit).")
        if answer.lower() == "q":
            break
        balance += spin(balance)

    print(f"You left with ${balance:.2f}")


if __name__ == "__main__":
    main()
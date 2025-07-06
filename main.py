import random
import os
from colorama import Fore, Style, init

# Initialize colorama for Windows compatibility
init()

# Game constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3
BALANCE_FILE = "balance.txt"  # File to save/load balance

# Symbol definitions and payout values
symbol_count = {
    "A": 2,
    "B": 3,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

# Game statistics for display
stats = {
    "games_played": 0,
    "total_won": 0,
    "total_lost": 0
}

# Save balance to file
def save_balance(balance):
    with open(BALANCE_FILE, "w") as f:
        f.write(str(balance))

# Load balance from file if it exists
def load_balance():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, "r") as f:
            return int(f.read())
    return None

# Determine winnings based on matching symbols on selected lines
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            line_win = values[symbol] * bet
            winnings += line_win
            winning_lines.append(line + 1)  # Line number (1-based)
    return winnings, winning_lines

# Generate a random slot machine spin (3x3 grid)
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        current_symbols = all_symbols[:]
        column = []
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

# Print the slot machine in a readable format with color for wins
def print_slot_machine(columns, winning_lines=[]):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            symbol = column[row]
            colored = Fore.GREEN + symbol + Style.RESET_ALL if (row + 1) in winning_lines else symbol
            end_char = " | " if i != len(columns) - 1 else ""
            print(colored, end=end_char)
        print()

# Ask user for initial deposit
def deposit():
    while True:
        amount = input("What would you like to deposit? $")
        if amount.isdigit() and int(amount) > 0:
            return int(amount)
        print("Please enter a positive number.")

# Ask how many lines to bet on (1-3)
def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit() and 1 <= int(lines) <= MAX_LINES:
            return int(lines)
        print("Please enter a valid number.")

# Ask for bet amount per line
def get_bet():
    while True:
        amount = input("What would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                return amount
            print(f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a number.")

# Play a single round of the slot machine
def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet <= balance:
            break
        print(f"Insufficient funds. Current balance: ${balance}")

    print(f"Betting ${bet} on {lines} lines. Total bet: ${total_bet}")
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)

    print_slot_machine(slots, winning_lines)
    print(f"You won ${winnings}.")
    if winnings >= bet * 10:
        print(Fore.YELLOW + "🎉 JACKPOT! Big win! 🎉" + Style.RESET_ALL)

    if winning_lines:
        print("Winning lines:", *winning_lines)
    else:
        print("No winning lines.")

    # Update game stats
    stats["games_played"] += 1
    net_gain = winnings - total_bet
    if net_gain >= 0:
        stats["total_won"] += net_gain
    else:
        stats["total_lost"] += -net_gain

    return net_gain

# Play multiple rounds automatically
def auto_spin(balance):
    while True:
        rounds = input("How many rounds would you like to auto-spin? ")
        if rounds.isdigit() and int(rounds) > 0:
            rounds = int(rounds)
            break
        print("Please enter a valid number.")

    for i in range(rounds):
        print(f"\n🔁 Auto-spin round {i + 1}/{rounds}")
        if balance < MIN_BET:
            print("Not enough balance to continue.")
            break
        balance += spin(balance)
        save_balance(balance)
        print(f"Balance: ${balance}")
    return balance

# Display current game statistics
def show_stats():
    print("\n📊 Game Statistics:")
    print(f"Games played: {stats['games_played']}")
    print(f"Total won: ${stats['total_won']}")
    print(f"Total lost: ${stats['total_lost']}")

# Entry point of the game
def main():
    balance = load_balance()
    if balance is None:
        balance = deposit()
    else:
        print(f"Loaded saved balance: ${balance}")

    while True:
        print(f"\n💰 Balance: ${balance}")
        print("1. Play")
        print("2. Auto-spin")
        print("3. Show stats")
        print("q. Quit")

        choice = input("Choose an option: ").strip().lower()
        if choice == "1":
            balance += spin(balance)
            save_balance(balance)
        elif choice == "2":
            balance = auto_spin(balance)
        elif choice == "3":
            show_stats()
        elif choice == "q":
            break
        else:
            print("Invalid choice.")

    print(f"\n👋 Thanks for playing! Final balance: ${balance}")
    save_balance(balance)
    show_stats()

if __name__ == "__main__":
    main()
#  Version 2
# Updated Application Works:
# Single Set Generation:
# The script asks if you want to input your own numbers.
# If you choose to input your own numbers, you can enter 7 unique numbers between 1 and 50.
# If you prefer a random set, the script generates one for you.

# Display:
# The generated set of 7 numbers is displayed as your Lotto Max ticket.
# This simplified version focuses solely on generating a single set of Lotto Max numbers, based on either your input or random generation.

import random

def generate_lotto_max_set(user_numbers=None):
    """Generates a set of 7 unique Lotto Max numbers (1-50), with an option for user input."""
    if user_numbers:
        return sorted(user_numbers)
    else:
        return sorted(random.sample(range(1, 51), 7))

def get_user_numbers():
    """Allows the user to input their own 7 numbers for the Lotto Max set."""
    user_numbers = []
    while len(user_numbers) < 7:
        try:
            number = int(input(f"Enter number {len(user_numbers) + 1} (between 1 and 50): "))
            if number < 1 or number > 50:
                print("Number must be between 1 and 50.")
            elif number in user_numbers:
                print("Duplicate number detected. Please enter a unique number.")
            else:
                user_numbers.append(number)
        except ValueError:
            print("Please enter a valid integer.")
    return sorted(user_numbers)

def generate_ticket():
    """Generates a Lotto Max ticket with a single set of 7 numbers."""
    # Ask if the user wants to input their own numbers
    use_user_numbers = input("Do you want to choose your Lotto Max numbers? (yes/no): ").lower()
    if use_user_numbers == "yes":
        user_numbers = get_user_numbers()
        ticket = generate_lotto_max_set(user_numbers)
    else:
        ticket = generate_lotto_max_set()

    # Display the ticket
    print("\nYour Lotto Max Numbers:")
    print(ticket)

# Run the ticket generator
generate_ticket()

#  Version 1
# Based on the rules you've provided,
# A Python application that generates Lotto Max numbers. 
# The application will include the following features:

# Generate Lotto Max Numbers:

# Generate 3 sets of 7 unique numbers each, ranging from 1 to 50.
# Allow the user to choose their first set of 7 numbers or randomly generate all 3 sets.
# Generate Extra Numbers: Generate up to 10 sets of 4 numbers each, ranging from 1 to 99.

# How the Application Works:
# 1- Lotto Max Sets:
# The script first asks the user if they want to input their own numbers for the first set.
# If the user chooses to input their numbers, it will allow them to input 7 unique numbers between 1 and 50.
# The script then generates two additional sets of random numbers.
# 2- Extra Numbers:
# The script asks the user if they want to include Extra numbers.
# If yes, the user can specify how many sets (1-10) of 4 Extra numbers they want.
# The script generates the specified number of Extra sets, with each number between 1 and 99.
# 3-Display:
# The ticket with all generated Lotto Max sets and Extra numbers (if any) is displayed.
# You can run this script and it will help you generate Lotto Max numbers according to the rules you provided.

import random

def generate_lotto_max_set():
    """Generates a set of 7 unique Lotto Max numbers (1-50)."""
    return sorted(random.sample(range(1, 51), 7))

def generate_extra_numbers():
    """Generates a set of 4 unique Extra numbers (1-99)."""
    return sorted(random.sample(range(1, 100), 4))

def get_user_numbers():
    """Allows the user to input their own 7 numbers for the first Lotto Max set."""
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
    """Generates a Lotto Max ticket with 3 sets of 7 numbers and up to 10 Extra numbers."""
    ticket = []

    # Ask if the user wants to input their own numbers for the first set
    use_user_numbers = input("Do you want to choose your first set of Lotto Max numbers? (yes/no): ").lower()
    if use_user_numbers == "yes":
        user_numbers = get_user_numbers()
        ticket.append(user_numbers)
    else:
        ticket.append(generate_lotto_max_set())

    # Generate the remaining two sets
    ticket.append(generate_lotto_max_set())
    ticket.append(generate_lotto_max_set())

    # Ask if the user wants to include Extra numbers
    include_extra = input("Do you want to include Extra numbers? (yes/no): ").lower()
    extra_numbers = []
    if include_extra == "yes":
        num_extra_sets = int(input("How many Extra sets would you like to generate? (1-10): "))
        for _ in range(num_extra_sets):
            extra_numbers.append(generate_extra_numbers())

    # Display the ticket
    print("\nLotto Max Ticket:")
    for i, numbers in enumerate(ticket, 1):
        print(f"Set {i}: {numbers}")

    if extra_numbers:
        print("\nExtra Numbers:")
        for i, numbers in enumerate(extra_numbers, 1):
            print(f"Extra Set {i}: {numbers}")

# Run the ticket generator
generate_ticket()

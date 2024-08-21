#  Version 3
# To consider these numbers in generating your Lotto Max ticket, 
# we have adjustment in the script to prioritize or include numbers from the most frequently drawn ones based on the frequency table you've provided.

# Explanation:
# Frequency Table: The script includes a frequency_table dictionary where keys are Lotto Max numbers, and values are their frequencies based on your provided screenshots.
# Weighted Random Selection: The function generate_weighted_random_number uses the random.choices method with weights to favor numbers that have been drawn more frequently.
# Set Generation: The generate_lotto_max_set function uses this weighted random number generator to produce a set of 7 unique numbers, prioritizing frequently drawn ones.

# How to Use:
# Run the script, and it will ask if you want to input your numbers. If not, it will generate a set of numbers considering the frequency data.
# The output will be a single set of 7 Lotto Max numbers.
# frequency_table is scrapped from the lotto max website 

import random
from lotto_max_scraper import LottoMaxScraper

scraper = LottoMaxScraper()
frequency_table = scraper.get_number_frequency_table()

def generate_weighted_random_number(frequency_table):
    """Generates a number based on its frequency in the table."""
    numbers = list(frequency_table.keys())
    frequencies = list(frequency_table.values())
    return random.choices(numbers, weights=frequencies, k=1)[0]

def generate_lotto_max_set(frequency_table, user_numbers=None):
    """Generates a set of 7 unique Lotto Max numbers (1-50), considering frequency."""
    if user_numbers:
        numbers_set = user_numbers
    else:
        numbers_set = set()

    while len(numbers_set) < 7:
        number = generate_weighted_random_number(frequency_table)
        if number not in numbers_set:
            numbers_set.add(number)

    return sorted(numbers_set)

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
    """Generates a Lotto Max ticket with a single set of 7 numbers, considering frequency."""
    # Ask if the user wants to input their own numbers
    use_user_numbers = input("Do you want to choose your Lotto Max numbers? (yes/no): ").lower()
    if use_user_numbers == "yes":
        user_numbers = get_user_numbers()
        ticket = generate_lotto_max_set(frequency_table, user_numbers)
    else:
        ticket = generate_lotto_max_set(frequency_table)

    # Display the ticket
    print("\nYour Lotto Max Numbers:")
    print(ticket)

# Run the ticket generator
generate_ticket()

#  Version 4
#  To incorporate the information from these tables into the Lotto Max number generator, 
#  we can adjust the script to consider the most common pairs, triplets, and sets of four numbers when generating the random numbers.
#  Here's how you can integrate these data sets into the calculations:
#  Step 1: Define the Common Pairs, Triplets, and Quads

# How This Works:
# Common Sets Selection: The script checks if there's enough space (less than 4 numbers chosen) to include a pair, triplet, or quad from your common sets. It prioritizes quads, then triplets, then pairs.
# Random Filling: After adding numbers from the common sets, the script fills the remaining slots with numbers generated using the weighted frequency method.

from lotto_max_scraper import LottoMaxScraper
import random

scraper = LottoMaxScraper()
frequency_table = scraper.get_number_frequency_table()
most_common_pairs = scraper.get_most_common_pairs()
most_common_consecutive_pairs = scraper.get_most_common_consecutive_pairs()
most_common_triplets = scraper.get_most_common_triplets()
most_common_consecutive_triplets = scraper.get_most_common_consecutive_triplets()
most_common_four_numbers = scraper.get_most_common_four_numbers()


def generate_weighted_random_number(frequency_table):
    """Generates a number based on its frequency in the table."""
    numbers = list(frequency_table.keys())
    frequencies = list(frequency_table.values())
    return random.choices(numbers, weights=frequencies, k=1)[0]

def select_from_common_sets(set_list, numbers_set, max_size):
    """Selects numbers from common pairs, triplets, or quads if space allows."""
    for num_set in set_list:
        if len(numbers_set) + len(num_set) <= max_size:
            if all(num not in numbers_set for num in num_set):
                numbers_set.update(num_set)
                if len(numbers_set) >= max_size:
                    break

def generate_lotto_max_set(frequency_table, user_numbers=None):
    """Generates a set of 7 unique Lotto Max numbers (1-50), considering frequency and common pairs/triplets."""
    numbers_set = set(user_numbers) if user_numbers else set()

    if len(numbers_set) < 4:
        select_from_common_sets(most_common_four_numbers, numbers_set, 4)
    
    if len(numbers_set) < 4:
        select_from_common_sets(most_common_triplets, numbers_set, 4)
    
    if len(numbers_set) < 4:
        select_from_common_sets(most_common_consecutive_triplets, numbers_set, 4)
    
    if len(numbers_set) < 4:
        select_from_common_sets(most_common_pairs, numbers_set, 4)
    
    if len(numbers_set) < 4:
        select_from_common_sets(most_common_consecutive_pairs, numbers_set, 4)

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
    """Generates a Lotto Max ticket with a single set of 7 numbers, considering frequency and common sets."""

    repeat = int(input("How many tickets do you like to buy?: "))
 
    for i in range(repeat):
        ticket = generate_lotto_max_set(frequency_table)
        print(ticket)

# Run the ticket generator
generate_ticket()

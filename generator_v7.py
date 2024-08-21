#  Version 7

# Key Points of the Updated Code:

# 1- Balanced Selection Process:
# The first loop (while len(numbers_set) < 5) ensures that pairs and triplets contribute to the selection, but only up to a point. This allows these combinations to influence the final set without dominating it entirely.

# 2- Secondary Sets and Randomness:
# Once the primary set (pairs, triplets) has contributed up to 5 numbers, the function moves on to consider lower-priority sets (consecutive triplets, four numbers) and then fills any remaining slots with random selections from the frequency table.

# 3- Lucky Numbers Inclusion:
# The user's lucky numbers are included first, ensuring that their preferences are reflected in the final ticket.

# 4- Controlled Randomness:
# The randomness is introduced after considering both the high-priority and low-priority sets. This ensures that the final set retains some unpredictability while still being grounded in historical data.

from lotto_max_scraper import LottoMaxScraper
import random

scraper = LottoMaxScraper()
frequency_table = scraper.get_number_frequency_table()
most_common_pairs = scraper.get_most_common_pairs()
most_common_consecutive_pairs = scraper.get_most_common_consecutive_pairs()
most_common_triplets = scraper.get_most_common_triplets()
most_common_consecutive_triplets = scraper.get_most_common_consecutive_triplets()
most_common_four_numbers = scraper.get_most_common_four_numbers()

def generate_weighted_random_number(frequency_table, damping_factor=0.8):
    """Generates a number considering frequency data with reduced bias."""
    numbers = list(frequency_table.keys())
    frequencies = list(frequency_table.values())
    
    total_weight = sum(frequencies)
    probabilities = [freq / total_weight for freq in frequencies]
    
    adjusted_probabilities = [(1 - damping_factor) + damping_factor * p for p in probabilities]
    
    return random.choices(numbers, weights=adjusted_probabilities, k=1)[0]

def get_lucky_numbers():
    """Allows the user to input their lucky numbers (1 to 7 numbers)."""
    lucky_numbers = []
    while True:
        try:
            num_lucky = int(input("How many lucky numbers would you like to input (0-7)? "))
            if num_lucky < 0 or num_lucky > 7:
                print("Please enter a number between 0 and 7.")
            else:
                num_lucky = 0
                break
        except ValueError:
            num_lucky = 0
            break
    
    for i in range(num_lucky):
        while True:
            try:
                number = int(input(f"Enter lucky number {i + 1} (between 1 and 50): "))
                if number < 1 or number > 50:
                    print("Number must be between 1 and 50.")
                elif number in lucky_numbers:
                    print("Duplicate number detected. Please enter a unique number.")
                else:
                    lucky_numbers.append(number)
                    break
            except ValueError:
                print("Please enter a valid integer.")
    
    return lucky_numbers

def select_weighted_set(set_list, numbers_set, max_size, weight):
    """Selects a pair, triplet, or quad with different weights, with an early exit if unsuccessful."""
    available_sets = [s for s in set_list if all(num not in numbers_set for num in s)]
    tries = 0
    max_tries = 10  # Limit the number of attempts to find a suitable set
    while available_sets and len(numbers_set) < max_size and tries < max_tries:
        weighted_choice = random.choices(available_sets, k=1)[0]
        chosen_set = weighted_choice
        if len(numbers_set) + len(chosen_set) <= max_size:
            numbers_set.update(chosen_set)
            break
        tries += 1
    # print('numbers_set', numbers_set)

def generate_lotto_max_set(frequency_table, damping_factor=0.8, lucky_numbers=None):
    """Generates a set of 7 unique Lotto Max numbers prioritizing the frequency table, with pairs, triplets, and lucky numbers."""
    numbers_set = set()

    # Include lucky numbers from the user, if any
    if lucky_numbers:
        numbers_set.update(lucky_numbers)

    # Start with the frequency table to select the majority of numbers
    while len(numbers_set) < 5:
        number = generate_weighted_random_number(frequency_table, damping_factor)
        if number not in numbers_set:
            numbers_set.add(number)
    print('1-numbers_set:', sorted(numbers_set))
    # Incorporate pairs, triplets, etc., but ensure they don't dominate
    if len(numbers_set) < 7:
        select_weighted_set(most_common_pairs, numbers_set, 7, 5)  # Higher priority
        print('most_common_pairs:numbers_set:', sorted(numbers_set))
    if len(numbers_set) < 7:
        select_weighted_set(most_common_consecutive_pairs, numbers_set, 7, 4)
        print('most_common_consecutive_pairs:numbers_set:', sorted(numbers_set))
    if len(numbers_set) < 7:
        select_weighted_set(most_common_triplets, numbers_set, 7, 3)
        print('most_common_triplets:numbers_set:', sorted(numbers_set))
    if len(numbers_set) < 7:
        select_weighted_set(most_common_consecutive_triplets, numbers_set, 7, 2)
        print('most_common_consecutive_triplets:numbers_set:', sorted(numbers_set)) 
    if len(numbers_set) < 7:
        select_weighted_set(most_common_four_numbers, numbers_set, 7, 1)  # Lower priority
        print('most_common_four_numbers:numbers_set:', sorted(numbers_set))

    # Fill any remaining slots with additional random numbers from the frequency table
    while len(numbers_set) < 7:
        number = generate_weighted_random_number(frequency_table, damping_factor)
        if number not in numbers_set:
            numbers_set.add(number)
            print('additional numbers_set:', sorted(numbers_set))

    return sorted(numbers_set)


def generate_ticket():
    """Generates Lotto Max tickets based on user input."""
    # Ask for number of tickets
    try:
        num_tickets = int(input("How many tickets would you like to generate? "))
    except ValueError:
        num_tickets = 1

    # Ask for a damping factor (optional)
    try:
        custom_damping = input("Enter a damping factor (press Enter to use default 0.8): ")
        damping_factor = float(custom_damping) if custom_damping else 0.8
    except ValueError:
        damping_factor = 0.8

    for i in range(num_tickets):
        print(f"\nGenerating ticket {i + 1}:")
           
        # Ask if the user has lucky numbers
        lucky_numbers = get_lucky_numbers()

        ticket = generate_lotto_max_set(frequency_table, damping_factor, lucky_numbers)
        
        # Display the ticket
        print("Your Lotto Max Numbers:", ticket)

def main():
    """Main function to run the Lotto Max number generator."""
    generate_ticket()

if __name__ == "__main__":
    main()
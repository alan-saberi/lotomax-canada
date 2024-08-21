#  Version 5
# Explanation:
# Damping Factor: The generate_weighted_random_number function now includes a damping factor to reduce the influence of frequently drawn numbers. This means even less frequent numbers have a fair chance of being selected.
# Random Selection of Common Sets: Instead of always using common pairs, triplets, or quads, this method randomly selects one or more from these sets, ensuring they don’t dominate the generated numbers.
# Balanced Influence: The overall approach introduces enough randomness to prevent the generated numbers from being overly biased towards historical patterns.
# Weights: By assigning different weights, the algorithm prioritizes the most common pairs, followed by consecutive pairs, triplets, and so forth. This way, the rarer combinations like triplets and quads have a lower influence, aligning with your preferences.
# Randomness: Despite the weights, the algorithm retains a level of randomness, ensuring that the generated numbers are not overly predictable.
# This updated strategy should provide a more balanced number generation, reflecting your desired priorities while minimizing bias. Feel free to test it out and adjust the weights or damping factors as needed!


# Key Features:
# 1- User Numbers: The user can choose to input their own numbers.
# 2- Multiple Tickets: The user specifies how many tickets they want to generate.
# 3- Custom Damping Factor: The user can provide a damping factor or use the default value of 0.8.

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

def select_weighted_set(set_list, numbers_set, max_size, weight):
    """Selects a pair, triplet, or quad with different weights."""
    available_sets = [s for s in set_list if all(num not in numbers_set for num in s)]
    if available_sets and len(numbers_set) < max_size:
        weighted_choice = random.choices(available_sets, k=weight)
        chosen_set = weighted_choice[0]
        if len(numbers_set) + len(chosen_set) <= max_size:
            numbers_set.update(chosen_set)

def generate_lotto_max_set(frequency_table, damping_factor=0.8, user_numbers=None):
    """Generates a set of 7 unique Lotto Max numbers considering frequency and weighted common sets."""
    numbers_set = set(user_numbers) if user_numbers else set()

    # Apply weighted influence based on the priority you provided
    if len(numbers_set) < 7:
        select_weighted_set(most_common_pairs, numbers_set, 7, 5)  # Highest weight
    if len(numbers_set) < 7:
        select_weighted_set(most_common_consecutive_pairs, numbers_set, 7, 4)
    if len(numbers_set) < 7:
        select_weighted_set(most_common_triplets, numbers_set, 7, 3)
    if len(numbers_set) < 7:
        select_weighted_set(most_common_consecutive_triplets, numbers_set, 7, 2)
    if len(numbers_set) < 7:
        select_weighted_set(most_common_four_numbers, numbers_set, 7, 1)  # Lowest weight

    while len(numbers_set) < 7:
        number = generate_weighted_random_number(frequency_table, damping_factor)
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
    return user_numbers

def generate_ticket():
    """Generates Lotto Max tickets based on user input."""
    # Ask for number of tickets
    num_tickets = int(input("How many tickets would you like to generate? "))

    # Ask for a damping factor (optional)
    custom_damping = input("Enter a damping factor (press Enter to use default 0.8): ")
    damping_factor = float(custom_damping) if custom_damping else 0.8

    for i in range(num_tickets):
        print(f"\nGenerating ticket {i + 1}:")
        
        ticket = generate_lotto_max_set(frequency_table, damping_factor)

        # Display the ticket
        print("Your Lotto Max Numbers:", ticket)

def main():
    """Main function to run the Lotto Max number generator."""
    generate_ticket()

if __name__ == "__main__":
    main()

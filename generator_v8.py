# Version 8

# Revised Approach:
# 1- Interleaved Selection:
# The function interleaves the selection process, allowing both the frequency table and the various combination sets (pairs, triplets, etc.) to contribute to the final set.

# 2- Balanced Contributions:
# By rotating through the different methods, the function ensures that all sources have a chance to contribute before the set is filled.

# 3- Final Random Fill:
# Any remaining slots after contributions from all sources are filled using random selections from the frequency table, ensuring the final set is balanced.

# Expected Outcome:
# This approach should prevent any single method (like frequency or pairs) from dominating the final set, allowing for a more balanced and diverse selection of numbers.
# The function should now successfully use all available data (frequency, pairs, triplets, etc.) without skipping over any sections.


from lotto_max_scraper import LottoMaxScraper
import random

scraper = LottoMaxScraper()
frequency_table = scraper.get_number_frequency_table()
most_common_pairs = scraper.get_most_common_pairs()
most_common_consecutive_pairs = scraper.get_most_common_consecutive_pairs()
most_common_triplets = scraper.get_most_common_triplets()
most_common_consecutive_triplets = scraper.get_most_common_consecutive_triplets()
most_common_four_numbers = scraper.get_most_common_four_numbers()

print('frequency_table:', frequency_table)
print('most_common_pairs:', most_common_pairs)
print('most_common_consecutive_pairs:', most_common_consecutive_pairs)
print('most_common_triplets:', most_common_triplets)
print('most_common_consecutive_triplets:', most_common_consecutive_triplets)
print('most_common_four_numbers:', most_common_four_numbers)


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
    """Generates a set of 7 unique Lotto Max numbers with balanced contributions from all sources."""
    numbers_set = set()

    # Include lucky numbers from the user, if any
    if lucky_numbers:
        numbers_set.update(lucky_numbers)
        print(f"Added lucky numbers: {lucky_numbers}")

    # Define the weighted sets and their corresponding weights
    weighted_sets = [
        (most_common_pairs, 5, "Most Common Pairs"),
        (most_common_consecutive_pairs, 4, "Most Common Consecutive Pairs"),
        (most_common_triplets, 3, "Most Common Triplets"),
        (most_common_consecutive_triplets, 2, "Most Common Consecutive Triplets"),
        (most_common_four_numbers, 1, "Most Common Four Numbers")
    ]
    
    # Ensure balanced contributions from frequency and combinations
    while len(numbers_set) < 7:
        if len(numbers_set) < 5:  # First, select a few numbers based on frequency
            number = generate_weighted_random_number(frequency_table, damping_factor)
            if number not in numbers_set:
                numbers_set.add(number)
                print(f"Added from frequency table: {number}")
        
        # Rotate through the weighted sets to add diversity
        for weighted_choice in weighted_sets:
            if len(numbers_set) < 7:
                set_name = weighted_choice[2]
                select_weighted_set(weighted_choice[0], numbers_set, 7, weighted_choice[1])
                print(f"Added from {set_name}: {sorted(numbers_set)}")
            else:
                break
    
    # Fill any remaining slots with random numbers from the frequency table
    while len(numbers_set) < 7:
        number = generate_weighted_random_number(frequency_table, damping_factor)
        if number not in numbers_set:
            numbers_set.add(number)
            print(f"Randomly added from frequency table to fill: {number}")

    print(f"Final generated set: {sorted(numbers_set)}\n")
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
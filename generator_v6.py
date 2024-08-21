#  Version 6

# Key Features:
# 1- User Numbers: The user can choose to input their own numbers.
# 2- Multiple Tickets: The user specifies how many tickets they want to generate.
# 3- Custom Damping Factor: The user can provide a damping factor or use the default value of 0.8.
# 4- Lucky Numbers: The get_lucky_numbers() function allows the user to input any number of "lucky" numbers (from 0 to 7). These numbers are guaranteed to be part of the generated set.

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

def generate_lotto_max_set(frequency_table, damping_factor=0.8, lucky_numbers=None):
    """Generates a set of 7 unique Lotto Max numbers considering frequency, weighted common sets, and lucky numbers."""
    numbers_set = set()

    if lucky_numbers:
        numbers_set.update(lucky_numbers)
    
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

def generate_ticket():
    """Generates Lotto Max tickets based on user input."""
    # Ask for number of tickets
    try:
        num_tickets = int(input("How many tickets would you like to generate? "))
    except:
        num_tickets = 1

    # Ask for a damping factor (optional)
    try:
        custom_damping = input("Enter a damping factor (press Enter to use default 0.8): ")
        if custom_damping: 
            damping_factor = float(custom_damping)
        else: 
            damping_factor = 0.8
    except:
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

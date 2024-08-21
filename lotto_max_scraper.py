# pip install beautifulsoup4
# pip install requests

import requests
from bs4 import BeautifulSoup
import re

class LottoMaxScraper:
    def __init__(self):
        self.base_url = "https://www.lotteryextreme.com/canada/"
        self.endpoints = {
            "number_frequency_table": "lottomax-statistics(1)",
            "most_common_pairs": "lottomax-statistics(5)",
            "most_common_consecutive_pairs": "lottomax-statistics(6)",
            "most_common_triplets": "lottomax-statistics(7)",
            "most_common_consecutive_triplets": "lottomax-statistics(8)",
            "most_common_four_numbers": "lottomax-statistics(9)",
        }

    def fetch_html_soup(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        html = response.text 
        soup = BeautifulSoup(html, "html.parser") 
        return soup

    def parse_frequency_numbers(self, soup):
        # Find the specific table by its style and content
        table = soup.find("table", {"style": "background:#dFdAbD;width:600px;margin-left:auto;margin-right:auto"})
        # Iterate over the rows of the table to extract numbers and their frequencies
        frequency_data = {}
        for row in table.find_all('tr')[2:]:  # Skip the first 2 rows to get to the data rows
            cols = row.find_all('td')
            if len(cols) >= 2:
                content = cols[0].text.strip()
                result = re.search("^(\d{1,})\s(\d{1,})", content)
                frequency_data[int(result.group(1))] = int(result.group(2))
        return frequency_data 

    def parse_most_common_pairs(self, soup):
        data = []
        outer_table = soup.find('table', style="background:#dFdAbD;width:600px;margin-left:auto;margin-right:auto")
        # Iterate over the rows and extract the relevant data
        for row in outer_table.find_all('tr', style="text-align:center;background:#FFFADD"):
            numbers_table = row.find('table', class_='results')
            numbers = [td.get_text() for td in numbers_table.find_all('td')]
            frequency = row.find_all('td', class_='f20')[0].get_text()
            entry = f"Numbers: {numbers}, Frequency: {frequency}"
            data.append(entry)
        return data
    
    def process_pair_data(self, data):
        most_common_pairs = []    
        for entry in data:
            try:
                if "Frequency:" in entry:
                    # Split the entry to extract numbers and frequency
                    numbers_str, frequency_str = entry.split("Frequency:")
                    # Extract all numbers from the numbers_str
                    numbers = re.findall(r'\d+', numbers_str)  
                    # Check if there are exactly two numbers in the list
                    if len(numbers) == 2:
                        # Convert them to integers and create a tuple
                        formatted_numbers = (int((int(numbers[0])-int(numbers[1]))/pow(10, len(numbers[1]))), int(numbers[1]))
                        # Append the tuple of numbers to the list
                        most_common_pairs.append(formatted_numbers)
                    else:
                        print(f"Error: Unexpected number format in entry: {entry}")
                        
                else:
                    print(f"Error: 'Frequency:' not found in entry: {entry}")
            except ValueError as e:
                print(f"Error processing entry: {entry}. Error: {e}")

        return most_common_pairs

    def parse_most_common_triplets(self, soup):
        # Find the table with the most common triplets
        table = soup.find('table', {'style': 'background:#dFdAbD;width:600px;margin-left:auto;margin-right:auto'})

        # Extract the rows containing triplets
        rows = table.find_all('tr', {'style': 'text-align:center;background:#FFFADD'})

        # List to store the most common triplets
        most_common_triplets = []

        # Loop through each row and extract the triplets
        for row in rows:
            # Find the table within the row that contains the triplet numbers
            numbers_table = row.find('table', class_='results')
            
            # Extract the numbers from the inner table
            numbers = [td.text.strip() for td in numbers_table.find_all('td')]
            number_2 = int(numbers[2])
            number_1 = int((int(numbers[1])-int(numbers[2]))/pow(10, len(numbers[2])))
            number_0 = int((int(numbers[0])-int(numbers[1]))/pow(10, len(numbers[1])))
            new_numbers = [number_0, number_1, number_2]            
            # Convert the numbers into a tuple and add it to the list
            most_common_triplets.append(tuple(new_numbers))

        return most_common_triplets
        
    def parse_most_common_four_numbers(self, soup):
        # Find the table with the most common triplets
        table = soup.find('table', {'style': 'background:#dFdAbD;width:600px;margin-left:auto;margin-right:auto'})
        rows = table.find_all('tr', {'style': 'text-align:center;background:#FFFADD'})

        # List to store the most common triplets
        most_common_four_numbers = []

        # Loop through each row and extract the triplets
        for row in rows:
            # Find the table within the row that contains the triplet numbers
            numbers_table = row.find('table', class_='results')
            
            # Extract the numbers from the inner table
            numbers = [td.text.strip() for td in numbers_table.find_all('td')]
            number_3 = int(numbers[3])
            number_2 = int((int(numbers[2])-int(numbers[3]))/pow(10, len(numbers[3])))
            number_1 = int((int(numbers[1])-int(numbers[2]))/pow(10, len(numbers[2])))
            number_0 = int((int(numbers[0])-int(numbers[1]))/pow(10, len(numbers[1]))) 
            new_numbers = [number_0, number_1, number_2, number_3]
            
            # Convert the numbers into a tuple and add it to the list
            most_common_four_numbers.append(tuple(new_numbers))

        return most_common_four_numbers
    
    def get_number_frequency_table(self):
        soup = self.fetch_html_soup(self.endpoints["number_frequency_table"])
        return self.parse_frequency_numbers(soup)
    
    def get_most_common_pairs(self):
        soup = self.fetch_html_soup(self.endpoints["most_common_pairs"])
        return self.process_pair_data(self.parse_most_common_pairs(soup))

    def get_most_common_consecutive_pairs(self):
        soup = self.fetch_html_soup(self.endpoints["most_common_consecutive_pairs"])
        return self.process_pair_data(self.parse_most_common_pairs(soup))
    
    def get_most_common_triplets(self):
        soup = self.fetch_html_soup(self.endpoints["most_common_triplets"])
        return self.parse_most_common_triplets(soup)

    def get_most_common_consecutive_triplets(self):
        soup = self.fetch_html_soup(self.endpoints["most_common_consecutive_triplets"])
        return self.parse_most_common_triplets(soup)
    
    def get_most_common_four_numbers(self):
        soup = self.fetch_html_soup(self.endpoints["most_common_four_numbers"])
        return self.parse_most_common_four_numbers(soup)

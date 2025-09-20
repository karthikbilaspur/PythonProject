import pandas as pd
import random

# Load the CSV file
def load_data(file_name):
    try:
        data = pd.read_csv("country-names.csv")
        return data
    except FileNotFoundError:
        print("File not found.")
        return None

# Calculate distance from North Pole and South Pole
def calculate_distance(data, country):
    latitude = country['y']
    distance_north = abs(90 - latitude)
    distance_south = abs(-90 - latitude)
    return distance_north, distance_south

# Main function
def main():
    file_name = 'country-names.csv'
    data = load_data(file_name)
    
    if data is not None:
        while True:
            random_country = random.choice(data.index)
            country = data.loc[random_country]
            distance_north, distance_south = calculate_distance(data.loc[random_country], country)
            
            print(f"Guess the country with the following distances:")
            print(f"Distance from North Pole: {distance_north} degrees")
            print(f"Distance from South Pole: {distance_south} degrees")
            
            guess = input("Enter your guess: ")
            if guess.lower() == country['country'].lower():
                print("Correct!")
            else:
                print(f"Sorry, the correct answer is {country['country']}.")
            
            play_again = input("Do you want to play again? (yes/no): ")
            if play_again.lower() != 'yes':
                break

if __name__ == "__main__":
    main()
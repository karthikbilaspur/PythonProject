import random
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Initialize the model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-base')
tokenizer = T5Tokenizer.from_pretrained('t5-base')

# Define a function to generate a story based on user input
def generate_story(user_input):
    input_ids = tokenizer.encode("generate story: " + user_input, return_tensors="pt")
    output = model.generate(input_ids, max_length=200)
    story = tokenizer.decode(output[0], skip_special_tokens=True)
    return story

# Define a function to get user input and respond with a story
def interactive_story_teller():
    print("Welcome to the interactive story teller!")
    user_name = input("What's your name? ")
    user_profile = {"name": user_name, "preferences": []}
    
    while True:
        print("\nMenu:")
        print("1. Generate a story")
        print("2. View profile")
        print("3. Quit")
        
        choice = input("What would you like to do? ")
        
        if choice == "1":
            user_input = input("Enter a prompt or type 'random' for a random story: ")
            if user_input.lower() == "random":
                user_input = random.choice(["adventure", "romance", "sci-fi", "fantasy"])
            story = generate_story(user_input)
            print("\nHere's a story based on your prompt:")
            print(story)
            
            user_choice = input("\nDo you want to continue the story? (yes/no): ")
            if user_choice.lower() == "yes":
                user_input = input("Enter a direction for the story: ")
                story = generate_story(user_input)
                print("\nHere's the continued story:")
                print(story)
            else:
                print("\nThanks for reading!")
                
            # Ask for user feedback
            feedback = input("\nHow would you rate this story? (1-5): ")
            user_profile["preferences"].append({"story": story, "rating": feedback})
            
        elif choice == "2":
            print("\nYour Profile:")
            print(f"Name: {user_profile['name']}")
            print("Preferences:")
            for preference in user_profile["preferences"]:
                print(f"Story: {preference['story'][:20]}... | Rating: {preference['rating']}")
                
        elif choice == "3":
            print("\nGoodbye!")
            break
            
        else:
            print("\nInvalid choice. Please try again.")

interactive_story_teller()
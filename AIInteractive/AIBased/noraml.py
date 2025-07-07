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
    while True:
        user_input = input("Enter a prompt or type 'quit' to exit: ")
        if user_input.lower() == "quit":
            break
        story = generate_story(user_input)
        print("Here's a story based on your prompt:")
        print(story)
        user_choice = input("Do you want to continue the story? (yes/no): ")
        if user_choice.lower() == "yes":
            user_input = input("Enter a direction for the story: ")
            story = generate_story(user_input)
            print("Here's the continued story:")
            print(story)
        else:
            print("Thanks for playing!")

interactive_story_teller()
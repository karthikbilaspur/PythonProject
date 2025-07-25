import json
import random
from transformers import T5Tokenizer, T5ForConditionalGeneration

class JokeGenerator:
    def __init__(self, filename, model_name='t5-small'):
        with open(filename, 'r') as f:
            self.data = json.load(f)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)

    def generate_joke_template(self):
        subject = random.choice(self.data['subjects'])
        action = random.choice(self.data['actions'])
        reason = random.choice(self.data['reasons'])

        joke = f"Why did the {subject} {action}? Because {reason}."
        return joke

    def generate_joke_t5(self, prompt):
        inputs = self.tokenizer.encode_plus(
            prompt,
            return_tensors="pt",
            max_length=50,
            truncation=True,
            padding="max_length",
        )

        output = self.model.generate(
            inputs["input_ids"],
            num_beams=4,
            no_repeat_ngram_size=2,
            min_length=10,
            max_length=50,
            early_stopping=True,
        )

        joke = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return joke

    def generate_joke(self, method='template', joke_type=None):
        if method == 'template':
            return self.generate_joke_template()
        elif method == 't5':
            if joke_type is None:
                joke_type = random.choice(self.data['joke_types'])
            prompt = self.data['joke_prompts'][joke_type]
            return self.generate_joke_t5(prompt)
        else:
            raise ValueError("Invalid method. Choose 'template' or 't5'.")

def main():
    joke_generator = JokeGenerator('jokes.json')
    print("Joke Generator")
    print("1. Generate joke using template")
    print("2. Generate joke using T5 model")
    print("3. Generate joke using T5 model with specific type")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        print(joke_generator.generate_joke('template'))
    elif choice == '2':
        print(joke_generator.generate_joke('t5'))
    elif choice == '3':
        print("Joke types:")
        for i, joke_type in enumerate(joke_generator.data['joke_types']):
            print(f"{i+1}. {joke_type}")
        joke_type_choice = int(input("Enter the number of your chosen joke type: "))
        joke_type = joke_generator.data['joke_types'][joke_type_choice - 1]
        print(joke_generator.generate_joke('t5', joke_type))
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
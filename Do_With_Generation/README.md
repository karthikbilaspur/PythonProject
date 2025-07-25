A Python-based joke generator that uses a JSON file to store joke templates and the T5 model to generate jokes.
Features
Template-based joke generation: Generate jokes using pre-defined templates and random subjects, actions, and reasons.
T5 model-based joke generation: Generate jokes using the T5 model and specific prompts.
Multiple joke types: Support for different joke types, including animal, food, travel, and sports.
Requirements
Python 3.x
transformers library
json library
Usage
Clone the repository and navigate to the project directory.
Install the required libraries using pip install transformers.
Run the joke_generator.py script.
Choose a joke generation method:
1: Generate joke using template
2: Generate joke using T5 model
3: Generate joke using T5 model with specific type
JSON File Format
The JSON file should contain the following keys:
subjects: List of subjects for template-based joke generation
actions: List of actions for template-based joke generation
reasons: List of reasons for template-based joke generation
joke_types: List of joke types for T5 model-based joke generation
joke_prompts: Dictionary of joke prompts for T5 model-based joke generation
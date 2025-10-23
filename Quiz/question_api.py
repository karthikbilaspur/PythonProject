import requests
import random

class QuestionAPI:
    def __init__(self):
        self.category_mappings = {"General Knowledge": 9, "Books": 10, "Movies": 11, "Music": 12, "Television": 14,
                                 "Video Games": 15, "Science and Nature": 17, "Computers": 18, "Mathematics": 19, "Mythology": 20, "Sports": 21,
                                 "Geography": 22, "History": 23, "Animals": 27, "Celebrities": 26, "Anime and Manga": 31,
                                 "Cartoons and Animations": 32, "Comics": 29}

    def get_questions(self, category, difficulty):
        if category == "Random Category":
            category = random.choice(list(self.category_mappings.keys()))
        category_id = self.category_mappings[category]
        url = f'https://opentdb.com/api.php?amount=10&category={category_id}&difficulty={difficulty.lower()}&type=multiple'
        response = requests.get(url)
        data = response.json()
        questions = [q['question'] for q in data['results']]
        options = [q['incorrect_answers'] + [q['correct_answer']] for q in data['results']]
        for i in range(len(options)):
            random.shuffle(options[i])
        correct_answers = [q['correct_answer'] for q in data['results']]
        return questions, options, correct_answers
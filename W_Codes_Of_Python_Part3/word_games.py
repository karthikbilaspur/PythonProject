import requests
import random
import time

class WordChainGame:
    def __init__(self):
        self.api_url = "https://api.datamuse.com/words"
        self.player_word = None
        self.computer_word = None
        self.api_requests = 0
        self.api_reset_time = time.time()

    def get_word(self, rel_rwc: str = None) -> str | None:
        self.check_api_rate_limit()
        try:
            params = {"rel_rwc": rel_rwc} if rel_rwc else {}
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()
            self.api_requests += 1
            return random.choice(data)['word']
        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
            return None

    def is_valid_word(self, word: str) -> bool:
        self.check_api_rate_limit()
        try:
            response = requests.get(self.api_url, params={"sp": word})
            response.raise_for_status()
            data = response.json()
            self.api_requests += 1
            return len(data) > 0
        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
            return False

    def get_next_word(self, word: str) -> str | None:
        self.check_api_rate_limit()
        try:
            response = requests.get(self.api_url, params={"rel_rwc": word})
            response.raise_for_status()
            data = response.json()
            self.api_requests += 1
            if len(data) > 0:
                return random.choice(data)['word']
            return None
        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
            return None

    def check_api_rate_limit(self):
        if self.api_requests >= 100:
            if time.time() - self.api_reset_time < 86400:
                print("API rate limit exceeded. Waiting for reset...")
                time.sleep(86400 - (time.time() - self.api_reset_time))
                self.api_requests = 0
                self.api_reset_time = time.time()
            else:
                self.api_requests = 0
                self.api_reset_time = time.time()

    def play(self):
        print("Welcome to Word Chain Game!")
        self.player_word = input("Enter a word: ")
        while True:
            if not self.is_valid_word(self.player_word):
                print("Invalid word! Try again.")
                self.player_word = input("Enter a word: ")
                continue
            self.computer_word = self.get_next_word(self.player_word)
            if self.computer_word is None:
                print("Computer can't think of a word. You win!")
                break
            print("Computer's word: ", self.computer_word)
            self.player_word = input("Enter a word: ")
            if not self.is_valid_word(self.player_word):
                print("Invalid word! Try again.")
                self.player_word = input("Enter a word: ")
                continue
            if self.player_word[0] != self.computer_word[-1]:
                print("Invalid word! Your word should start with the last letter of the computer's word.")
                self.player_word = input("Enter a word: ")

if __name__ == "__main__":
    game = WordChainGame()
    game.play()
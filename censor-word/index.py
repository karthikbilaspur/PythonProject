from profanity_check import predict, predict_prob
from better_profanity import profanity
import re

class ProfanityDetector:
    def __init__(self, censor_char="*"):
        self.censor_char = censor_char
        self.whitelist = set()

    def detect_censor_words(self, text, method="hybrid"):
        """
        Detects censor words in a given text and returns the censored text.

        Args:
            text (str): The input text to check for censor words.
            method (str): The method to use for censoring (default is "hybrid").
                          Options: "profanity_check", "better_profanity", "hybrid"

        Returns:
            str: The censored text if censor words are detected, otherwise the original text.
        """
        # Preprocess text
        original_text = text
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)

        # Check for profanity
        prediction = predict([text])
        probability = predict_prob([text])
        if prediction[0] == 1:
            print(f"Censor word detected with probability: {probability[0]}")
            # Censor the text
            if method == "profanity_check":
                censored_text = self.censor_with_profanity_check(original_text)
            elif method == "better_profanity":
                censored_text = profanity.censor(original_text)
            else:  # hybrid
                censored_text = self.censor_with_profanity_check(original_text)
                censored_text = profanity.censor(censored_text)
            return censored_text
        else:
            print("No censor words detected")
            return original_text

    def censor_with_profanity_check(self, text):
        censored_text = ""
        words = text.split()
        for word in words:
            if predict([word.lower()])[0] == 1:
                censored_text += self.censor_char * len(word) + " "
            else:
                censored_text += word + " "
        return censored_text.strip()

    def add_to_whitelist(self, word):
        self.whitelist.add(word)

def main():
    detector = ProfanityDetector()
    text = input("Enter text to check for censor words: ")
    print("Choose a censoring method:")
    print("1. Profanity Check")
    print("2. Better Profanity")
    print("3. Hybrid")
    choice = input("Enter your choice (1/2/3): ")
    if choice == "1":
        censored_text = detector.detect_censor_words(text, method="profanity_check")
    elif choice == "2":
        censored_text = detector.detect_censor_words(text, method="better_profanity")
    else:
        censored_text = detector.detect_censor_words(text, method="hybrid")
    print("Censored Text:", censored_text)

if __name__ == "__main__":
    main()
import random
import string

def speak_like_yoda(sentence: str) -> None:
    """
    Translate the input sentence into Yoda-speak.

    :param sentence: input string
    :return: translation to Yoda-speak
    """
    # Convert to lowercase and remove punctuation
    sentence = sentence.lower()
    translator = str.maketrans('', '', string.punctuation.replace("'", ''))
    sentence = sentence.translate(translator)

    # Split into words and shuffle
    words = sentence.split()
    random.shuffle(words)

    # Reconstruct sentence with Yoda-like syntax
    new_sent = ''
    for i, word in enumerate(words):
        if i == 0:
            new_sent += word.capitalize()
        elif i == len(words) - 1:
            new_sent += ' ' + word + '.'
        else:
            new_sent += ' ' + word

    # Add some Yoda-like phrases
    yoda_phrases = ['A long time, I have waited.', 'Much to learn, you still have.', 'Patience, young one.']
    if random.random() < 0.5:
        new_sent += ' ' + random.choice(yoda_phrases)

    print('\nYour Yodenglish sentence: ')
    print(new_sent)


if __name__ == '__main__':
    print('Enter your English sentence: ')
    sentence = input()
    speak_like_yoda(sentence)
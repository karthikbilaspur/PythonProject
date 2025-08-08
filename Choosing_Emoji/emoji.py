import requests

class EmojiAPI:
    def __init__(self):
        self.base_url = "https://emoji-api.com/emojis"

    def get_emojis(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            return response.json()
        else:
            return []

    def get_emoji(self, slug):
        response = requests.get(f"{self.base_url}/{slug}")
        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def search_emojis(self, query):
        emojis = self.get_emojis()
        return [emoji for emoji in emojis if query.lower() in emoji['slug'].lower() or query.lower() in emoji['character'].lower()]

def text_to_emoji(text, emojis):
    words = text.split()
    emoji_text = ""
    for word in words:
        for emoji in emojis:
            if word.lower() in emoji['slug'].lower():
                emoji_text += emoji['character'] + " "
                break
        else:
            emoji_text += word + " "
    return emoji_text.strip()

def emoji_to_text(emoji_text, emojis):
    text = ""
    for emoji_char in emoji_text:
        for emoji in emojis:
            if emoji_char == emoji['character']:
                text += emoji['slug'] + " "
                break
        else:
            text += emoji_char + " "
    return text.strip()

def main():
    emoji_api = EmojiAPI()
    emojis = emoji_api.get_emojis()

    while True:
        print("\nEmoji Converter Menu:")
        print("1. Text to Emoji")
        print("2. Emoji to Text")
        print("3. Search Emojis")
        print("4. Quit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            text = input("Enter text: ")
            print(text_to_emoji(text, emojis))
        elif choice == "2":
            emoji_text = input("Enter emoji text: ")
            print(emoji_to_text(emoji_text, emojis))
        elif choice == "3":
            query = input("Enter search query: ")
            search_results = emoji_api.search_emojis(query)
            for emoji in search_results:
                print(f"{emoji['character']} - {emoji['slug']}")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
import requests
from typing import TypedDict, cast


class Emoji(TypedDict, total=False):
    character: str
    slug: str

class EmojiAPI:
    def __init__(self) -> None:
        self.base_url = "https://emoji-api.com/emojis"

    def get_emojis(self) -> list[Emoji]:
        response = requests.get(self.base_url)
        if response.status_code == 200:
            return cast(list[Emoji], response.json())
        else:
            return []

    def get_emoji(self, slug: str) -> Emoji:
        response = requests.get(f"{self.base_url}/{slug}")
        if response.status_code == 200:
            return cast(Emoji, response.json())
        else:
            return {}

    def search_emojis(self, query: str) -> list[Emoji]:
        emojis = self.get_emojis()
        query_lower = query.lower()
        return [
            emoji for emoji in emojis
            if query_lower in emoji.get("slug", "").lower()
            or query_lower in emoji.get("character", "").lower()
        ]

def text_to_emoji(text: str, emojis: list[Emoji]) -> str:
    words = text.split()
    converted: list[str] = []
    for word in words:
        for emoji in emojis:
            if word.lower() in emoji.get("slug", "").lower():
                converted.append(emoji.get("character", ""))
                break
        else:
            converted.append(word)
    return " ".join(converted)

def emoji_to_text(emoji_text: str, emojis: list[Emoji]) -> str:
    converted: list[str] = []
    for emoji_char in emoji_text:
        for emoji in emojis:
            if emoji_char == emoji.get("character", ""):
                converted.append(emoji.get("slug", ""))
                break
        else:
            converted.append(emoji_char)
    return " ".join(converted)

def main() -> None:
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
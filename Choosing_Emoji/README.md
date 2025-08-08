# Choosing Emoji

This Python script uses the Emoji API to fetch and utilize emojis in a text-based emoji converter application. Here's a breakdown of the code:
Key Features:
Emoji API Integration: Fetches emojis from the Emoji API and uses them for text-to-emoji and emoji-to-text conversions.
Text-to-Emoji Conversion: Replaces words in text with corresponding emojis.
Emoji-to-Text Conversion: Replaces emojis with their corresponding text representations (slugs).
Emoji Search: Allows users to search for emojis based on a query.
Code Structure:
EmojiAPI Class: Handles interactions with the Emoji API, including fetching emojis and searching for specific emojis.
Conversion Functions: text_to_emoji and emoji_to_text functions perform the conversions using the fetched emojis.
Main Function: Provides a menu-driven interface for users to choose between text-to-emoji conversion, emoji-to-text conversion, emoji search, or quitting the program.
Output:
The script displays the converted text or search results based on the user's choice.

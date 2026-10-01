# Blackjack Game Summary

This code implements a game of Blackjack, a popular casino card game. The game allows a single player to play against the dealer.
Key Features:
Deck Creation: A deck of 52 cards is created and shuffled.
Card Dealing: The player and dealer are each dealt two cards.
Player's Turn: The player can choose to either "hit" (take another card) or "stand" (keep their current hand).
Dealer's Turn: After the player stands, the dealer draws cards until their hand value is 17 or higher.
Win/Loss Conditions: The game determines the winner based on the final hand values, with the player winning if their hand value is higher without exceeding 21.
Gameplay:
The player is presented with their hand and the dealer's up card.
The player can choose to hit or stand.
If the player's hand value exceeds 21, they lose.
After the player stands, the dealer's hand is revealed, and they draw cards according to their strategy.
The game determines the winner and announces the result.
Code Structure:
The code is organized into classes for Card, Deck, Hand, Player, and Dealer, making it easy to understand and maintain. The game logic is implemented using methods within these classes. The main game loop is controlled by the play_blackjack function, which orchestrates the gameplay.

import random

# Define card ranks and suits
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Define card values
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for r in ranks for s in suits]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_hand_value(self):
        value = sum([values[card.rank] for card in self.cards])
        # Adjust value if hand contains Aces
        for card in self.cards:
            if card.rank == 'A' and value > 21:
                value -= 10
        return value

    def __str__(self):
        return f"Hand value: {self.calculate_hand_value()}\nCards: {[str(card) for card in self.cards]}"

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = Hand()

    def hit(self, deck):
        self.hand.add_card(deck.deal_card())

    def stand(self):
        pass

class Dealer(Player):
    def play(self, deck):
        while self.hand.calculate_hand_value() < 17:
            self.hit(deck)

def play_blackjack():
    deck = Deck()
    player = Player("Player")
    dealer = Dealer("Dealer")

    player.hit(deck)
    player.hit(deck)

    dealer.hit(deck)
    dealer.hit(deck)

    print("Your hand:")
    print(player.hand)
    print("\nDealer's up card:")
    print(dealer.hand.cards[0])

    while True:
        action = input("\nDo you want to 'hit' or 'stand'? ")
        if action.lower() == 'hit':
            player.hit(deck)
            print("\nYour hand:")
            print(player.hand)
            if player.hand.calculate_hand_value() > 21:
                print("You busted! Dealer wins.")
                return
        elif action.lower() == 'stand':
            player.stand()
            break
        else:
            print("Invalid input. Please enter 'hit' or 'stand'.")

    dealer.play(deck)

    print("\nYour hand:")
    print(player.hand)
    print("\nDealer's hand:")
    print(dealer.hand)

    if dealer.hand.calculate_hand_value() > 21:
        print("Dealer busted! You win.")
    elif dealer.hand.calculate_hand_value() < player.hand.calculate_hand_value():
        print("Your total is higher. You win.")
    elif dealer.hand.calculate_hand_value() > player.hand.calculate_hand_value():
        print("Dealer's total is higher. Dealer wins.")
    else:
        print("It's a tie.")

def main():
    play_again = 'y'
    while play_again.lower() == 'y':
        play_blackjack()
        play_again = input("\nDo you want to play again? (y/n): ")
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
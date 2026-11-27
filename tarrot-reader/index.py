import random
import datetime
import json
import os

# --- Deck: name -> (upright meaning, reversed meaning) ---
TAROT_DECK = {
    "The Fool": ("Experience is your best teacher", "You're ignoring the lesson - again"),
    "The Magician": ("Life is Magic... do you control yours?", "You're letting someone else pull the strings"),
    "The High Priestess": ("Stay away from worldly affairs", "You're ignoring your intuition"),
    "The Empress": ("The world bows before you, you bow to none", "You're giving too much and getting nothing back"),
    "The Emperor": ("The world bows before you, you bow to none", "Control is slipping - or you're gripping too hard"),
    "The Hierophant": ("Follow the 4rc@n3 principles", "Question the rules you were taught"),
    "The Lovers": ("I've never writ, nor no man never loved", "A choice is being avoided"),
    "The Chariot": ("You'll get to see your dream ride soon", "You're being pulled in two directions"),
    "Strength": ("You are strong enough", "You're being harder on yourself than you need to be"),
    "The Hermit": ("The World hurtles forward, yet you remain uncaught in its riptide", "Isolation is becoming loneliness"),
    "Wheel of Fortune": ("Your luck today depends on whether the first living thing you see is a plant or an animal", "The wheel is stuck - break the pattern"),
    "Justice": ("The Mills of God grind slow but fine", "Something unfair needs to be named"),
    "The Hanged Man": ("That's rough buddy", "Let go - you're the one holding on"),
    "Death": ("Life's younger sibling brushed your shoulder just now, but you're fine - it was just lint", "You're resisting a change that already happened"),
    "Temperance": ("The World needs more of it, and of you", "Balance is off - too much of one thing"),
    "The Devil": ("Get over here so I can prove that you exist", "A habit has you, not the other way round"),
    "The Tower": ("Exchange places with the king", "The shake-up is coming whether you like it or not"),
    "The Star": ("Like diamonds in the sky~", "Hope feels far away - look again"),
    "The Moon": ("You might find that your enthusiasm waxes and wanes, but that's alright", "Something isn't what it seems"),
    "The Sun": ("You're the light of someone's life", "You're dimming yourself to fit in"),
    "Judgement": ("*judges you in Spanish*", "*judges you even harder in Spanish*"),
    "The World": ("These hands could hold you but it'll never be enough~", "You're almost there - don't quit at the last step"),
    "Ace of Wands": ("You're a wizard, Harry", "The spark is there, but no action yet"),
    "Two of Wands": ("Your sibling is pretty cool", "You're stuck between staying and leaving"),
    "Three of Wands": ("Try to avoid tournaments for the time being", "Your plans need more patience"),
    "Four of Wands": ("Find trouble and make it double", "Celebrate - you earned it, even if it feels small"),
    "Five of Wands": ("Expecto Patronum!", "Too many opinions, not enough listening"),
    "Six of Wands": ("Draw your wand", "Victory is coming - don't downplay it"),
    "Seven of Wands": ("If you see a noseless man with the complexion of crushed eggshells, RUN", "You're defending yourself too much"),
    "Eight of Wands": ("I'm surprised you got this tbh... I'll let you in on a secret - Seven didn't actually eat Nine", "Messages are delayed - wait a little"),
    "Nine of Wands": ("Oh, the card you're looking for is 3 quarters to the right", "You're tired because you never put the wand down"),
    "Ten of Wands": ("Oh, the card you're looking for is a quarter to the left", "Put something down. Seriously."),
    "Page of Wands": ("You're going to be called to the Head's Office - you shouldn't have messed with alchemy unsupervised", "A new idea is being ignored"),
    "Knight of Wands": ("You just had to buy that giant chess set, didn't you?", "Slow down before you burn out"),
    "Queen of Wands": ("With great power...", "...comes great need for a nap"),
    "King of Wands": ("With great power...", "...comes great responsibility to actually rest"),
    "Ace of Cups": ("If you ever see a trophy in the middle of a hedge maze...", "Your heart is guarded for a reason - check if it's still needed"),
    "Two of Cups": ("Bottoms up, friend!", "A connection needs honest talk"),
    "Three of Cups": ("Two's company, three's better company!", "Call your friends - they miss you"),
    "Four of Cups": ("The more the merrier!", "You're missing an offer right in front of you"),
    "Five of Cups": ("Yeah, social distancing is important", "You're staring at what's spilled, not what's left"),
    "Six of Cups": ("Now that's one too many", "Nostalgia is lying to you a little"),
    "Seven of Cups": ("Two's company enough", "Too many options - pick one"),
    "Eight of Cups": ("Take a break", "Walking away is the brave move here"),
    "Nine of Cups": ("If three's a crowd...", "Wish granted - now what?"),
    "Ten of Cups": ("Stop it now", "Happiness is here, stop waiting for the catch"),
    "Page of Cups": ("I don't think you should drive until you clear your head", "Feelings are talking - listen"),
    "Knight of Cups": ("Put that sword down right this instant", "Romance is clouding judgement"),
    "Queen of Cups": ("Don't offend anyone influential", "You're absorbing everyone else's feelings"),
    "King of Cups": ("Don't get on your gaurdians' bad side", "Stay calm - you're the steady one"),
    "Ace of Swords": ("Draw your sword", "The truth will sting - say it anyway"),
    "Two of Swords": ("En garde", "You're avoiding a decision"),
    "Three of Swords": ("Allez!", "Heartbreak is healing, slowly"),
    "Four of Swords": ("Parry!", "Rest. The battle can wait."),
    "Five of Swords": ("Learn enough to be dangerous", "Winning this argument will cost too much"),
    "Six of Swords": ("Get yourself a teacher", "You're leaving something behind - it's time"),
    "Seven of Swords": ("Parlay!", "Someone isn't being straight with you"),
    "Eight of Swords": ("Do something nice for a stranger", "The cage is mostly in your head"),
    "Nine of Swords": ("Be chivalrous", "The 3am worries are louder than reality"),
    "Ten of Swords": ("I'm not asking for much, just be nice", "Rock bottom - the only way is up now"),
    "Page of Swords": ("The pen is mightier", "Think before you send that message"),
    "Knight of Swords": ("Live by the code you're honour-bound to follow", "Charging ahead without a plan"),
    "Queen of Swords": ("Pledge alliance", "Be honest, even if it's blunt"),
    "King of Swords": ("Pledge alliance", "Logic over emotion - for now"),
    "Ace of Coins": ("You now have an iron nail", "A new opportunity - small, but real"),
    "Two of Coins": ("Flip a coin", "You're juggling too much"),
    "Three of Coins": ("For want of a nail...", "Teamwork will get this done"),
    "Four of Coins": ("You now have a paperclip", "You're holding on too tight"),
    "Five of Coins": ("Sleep well, it is a blessing", "Ask for help - it's not weakness"),
    "Six of Coins": ("Roll a die", "Give - or receive - generously"),
    "Seven of Coins": ("You're a lucky one", "Results are slow, not absent"),
    "Eight of Coins": ("You're like a pineapple tree - i.e. you're a factual error", "Practice is paying off, keep going"),
    "Nine of Coins": ("Accessory fruit (affectionate)", "Enjoy what you built alone"),
    "Ten of Coins": ("<insert cool fruit fact here>", "Family / money stress - talk about it"),
    "Page of Coins": ("You're due for a promotion soon", "Learn the boring skill - it pays off"),
    "Knight of Coins": ("Treat your subordinates", "Slow and steady is still progress"),
    "Queen of Coins": ("You're worth your weight in gold", "Take care of yourself like you take care of others"),
    "King of Coins": ("You're worth your weight in gold", "Build something that lasts"),
}

SPREADS = {
    "1": ("Single Card - Daily Guidance", ["Your card"]),
    "2": ("Three Cards - Past / Present / Future", ["Past", "Present", "Future"]),
    "3": ("Five Cards - Situation / Challenge / Advice / Hidden / Outcome", ["Situation", "Challenge", "Advice", "Hidden Influence", "Outcome"]),
}

HISTORY_FILE = "tarot_history.json"

def pause(prompt: str = ">> press enter") -> None:
    input(prompt)

def draw_cards(deck: dict[str, tuple[str, str]], num: int) -> list[dict[str, str | bool]]:
    names = random.sample(list(deck.keys()), num)
    drawn: list[dict[str, str | bool]] = []
    for name in names:
        reversed_card = random.random() < 0.3  # 30% chance reversed
        upright, reversed_meaning = deck[name]
        drawn.append({
            "name": name,
            "reversed": reversed_card,
            "meaning": reversed_meaning if reversed_card else upright,
        })
    return drawn

def print_card(position: str, card: dict[str, str | bool]) -> None:
    label = f"{card['name']} (Reversed)" if card['reversed'] else card['name']
    print(f"  Your {position} card is...")
    print(f"  --- {label} ---")
    print(f"  {card['meaning']}")
    print()

def save_reading(spread_name: str, cards: list[dict[str, str | bool]], question: str) -> None:
    entry = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "question": question,
        "spread": spread_name,
        "cards": cards,
    }
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE) as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def show_history():
    if not os.path.exists(HISTORY_FILE):
        print("\nNo past readings yet. The cards await...")
        return
    with open(HISTORY_FILE) as f:
        history = json.load(f)
    print(f"\n--- Past Readings ({len(history)}) ---")
    for h in history[-5:]:  # last 5 only
        print(f"\n{h['date']} | {h['spread']} | Q: {h['question'] or '(none)'}")
        for c in h['cards']:
            rev = " (Reversed)" if c['reversed'] else ""
            print(f"  - {c['name']}{rev}: {c['meaning']}")

def do_reading():
    print("\nChoose your spread:")
    for key, (name, _) in SPREADS.items():
        print(f"  {key}. {name}")
    choice = input(">> pick 1 / 2 / 3: ").strip()
    if choice not in SPREADS:
        print("The cards reject that choice. Pick 1, 2 or 3.")
        return
    spread_name, positions = SPREADS[choice]
    question = input(">> whisper your question (or press enter to skip): ").strip()
    print(f"\n--- {spread_name} ---")
    if question:
        print(f"Question: {question}")
    print("Shuffling...")
    pause()
    cards = draw_cards(TAROT_DECK, len(positions))
    for pos, card in zip(positions, cards):
        print_card(pos, card)
        pause()
    save_reading(spread_name, cards, question)
    print("Reading saved to tarot_history.json")

def youve_chosen_yes():
    print("I see that you've chosen to divine your future....")
    pause()
    print("Let's make haste then...")
    pause()
    print("Neither fame nor fortune wait for man")
    pause()
    do_reading()

def youve_chosen_no():
    print("Are you wise...")
    pause()
    print("Or foolish?")
    pause()
    print("I suppose only time will tell")
    pause()

def youve_chosen_neither():
    print("*le sigh*")
    pause()
    print("I suppose you think this is a game...")
    pause()
    print("You wouldn't be wrong...")
    pause()
    print("But the only thing that you've played...")
    pause()
    print("Is yourself.")
    pause()
    print("\nNever gonna give you up,\nNever gonna let you down,\nNever gonna run around and desert you.\nNever gonna make you cry,\nNever gonna say goodbye,\nNever gonna tell a lie and hurt you.\n")

def main():
    print("In this black box, you read white words")
    pause()
    print("Words that might warn you of danger...")
    pause()
    print("Words that might foretell great fortune...")
    pause()
    print("Or words that might make you laugh")
    pause()
    print()
    while True:
        print("\n1. Draw a card (Y)")
        print("2. Refuse (n)")
        print("3. History")
        print("4. Quit")
        ch = input(">> enter Y/n, 3 for history, 4 to quit: ").strip().lower()
        print("\nInteresting...")
        if ch in ("y", "yes", "1"):
            youve_chosen_yes()
        elif ch in ("n", "no", "2"):
            youve_chosen_no()
        elif ch == "3":
            show_history()
        elif ch in ("4", "q", "quit", "exit"):
            break
        else:
            youve_chosen_neither()
        print("\nWhichever your choice was...")
        pause()
        print("May the cards ever be in your favour")
        pause()
    print()
    print("\x1B[3mFin\x1B[23m".center(72))
    print("*" * 72)

if __name__ == "__main__":
    main()

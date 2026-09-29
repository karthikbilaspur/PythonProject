# AI Adjective Comparative & Superlative Generator
# Beginner Friendly - 1 Page Version

IRREGULAR = {
    "good": ("better", "best"),
    "bad": ("worse", "worst"),
    "far": ("farther", "farthest"),
    "little": ("less", "least"),
    "many": ("more", "most"),
    "much": ("more", "most"),
}

def count_syllables(word: str) -> int:
    """Simple AI trick: count vowel groups to guess syllables"""
    word = word.lower()
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e"):
        count -= 1
    return max(1, count)

def get_forms(adjective: str) -> tuple[str, str]:
    adj = adjective.lower().strip()

    # 1. Irregular
    if adj in IRREGULAR:
        return IRREGULAR[adj]

    # 2. Long adjectives (3+ syllables) -> more / most
    if count_syllables(adj) >= 3:
        return f"more {adj}", f"most {adj}"

    # 3. Ends with y -> happier / happiest
    if adj.endswith("y") and adj[-2] not in "aeiou":
        base = adj[:-1]
        return f"{base}ier", f"{base}iest"

    # 4. Ends with e -> nicer / nicest
    if adj.endswith("e"):
        return f"{adj}r", f"{adj}st"

    # 5. CVC pattern (big -> bigger) - double last consonant
    if len(adj) >= 3 and adj[-1] not in "aeiouwxy" and adj[-2] in "aeiou" and adj[-3] not in "aeiou":
        return f"{adj}{adj[-1]}er", f"{adj}{adj[-1]}est"

    # 6. Default -> taller / tallest
    # Some 2-syllable words still sound better with more/most, we offer both
    if count_syllables(adj) == 2:
        return f"{adj}er / more {adj}", f"{adj}est / most {adj}"

    return f"{adj}er", f"{adj}est"

# --- Main App Loop ---
def main():
    print("=== AI Adjective Generator (comparative & superlative) ===")
    print("Type 'quit' to exit\n")

    while True:
        word = input("Enter an adjective: ").strip()
        if word.lower() in ["quit", "exit", "q"]:
            break
        if not word.isalpha():
            print("Please enter letters only.\n")
            continue

        comp, sup = get_forms(word)
        print(f" -> Comparative: {comp}")
        print(f" -> Superlative: {sup}\n")

if __name__ == "__main__":
    main()
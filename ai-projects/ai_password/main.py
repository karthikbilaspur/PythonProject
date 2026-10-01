"""
main.py - CLI for Extreme Password AI
"""
from password_engine import ExtremePasswordAI
from strength_analyzer import StrengthAnalyzer

def banner():
    print("""
    ╔════════════════════════════════════╗
    ║  EXTREME PASSWORD AI - SECURE     ║
    ║  Secure + Markov + Pattern + Mem  ║
    ╚════════════════════════════════════╝
    """)

def main():
    banner()
    engine = ExtremePasswordAI(length=12)
    analyzer = StrengthAnalyzer()

    # Train Markov with default list
    default_passwords = ["P@ssw0rd!", "S3cur1ty!", "Str0ngP@ssw0rd!", "C0mpl3x!ty123", "MyS3cur3P@ss"]
    engine.train(default_passwords)

    while True:
        print("\n--- EXTREME MENU ---")
        print("1. Generate Secure Password [FIXED FILE 1]")
        print("2. Generate Markov Password [FIXED FILE 2]")
        print("3. Generate from Pattern [FIXED FILE 3]")
        print("4. Generate Memorable (Correct-Horse) [NEW EXTREME]")
        print("5. Generate EXTREME (best of all) [NEW EXTREME]")
        print("6. Check Password Strength")
        print("7. Train Markov Model")
        print("8. Bulk Generate (10 passwords)")
        print("0. Exit")

        choice = input("> ").strip()

        if choice == "1":
            length = int(input("Length [12]: ") or 12)
            use_upper = input("Uppercase? y/n [y]: ").lower() != 'n'
            use_digits = input("Digits? y/n [y]: ").lower() != 'n'
            use_symbols = input("Symbols? y/n [y]: ").lower() != 'n'
            try:
                pwd = engine.generate_secure(length, use_upper, use_digits, use_symbols)
                print(f"\nGenerated: {pwd}")
                print(analyzer.check_strength(pwd))
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            pwd = engine.generate_markov()
            print(f"\nMarkov: {pwd}")
            print(analyzer.check_strength(pwd))

        elif choice == "3":
            print("Legend: L=lower, U=upper, D=digit, S=symbol")
            print("Example: ULLDDS -> Ab12!@ , U-U-L-L-D-D -> A-B-c-d-1-2")
            pattern = input("Pattern [ULLDDS]: ") or "ULLDDS"
            try:
                pwd = engine.generate_from_pattern(pattern)
                print(f"\nPattern: {pwd}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            words = int(input("How many words? [4]: ") or 4)
            pwd = engine.generate_memorable(words=words)
            print(f"\nMemorable: {pwd}")
            print(analyzer.check_strength(pwd))

        elif choice == "5":
            length = int(input("Length [16]: ") or 16)
            pwd = engine.generate_extreme(length)
            print(f"\nEXTREME: {pwd}")
            print(analyzer.check_strength(pwd))

        elif choice == "6":
            pwd = input("Enter password to check: ")
            result = analyzer.check_strength(pwd)
            print(f"\nLabel: {result['label']} ({result['score']}/{result['max_score']})")
            print(f"Entropy: {result['entropy_bits']} bits - Crack time: {result['crack_time']}")
            if result['errors']:
                print("Fix:")
                for e in result['errors']:
                    print(f" - {e}")

        elif choice == "7":
            pwds = input("Enter passwords comma separated to train: ").split(',')
            pwds = [p.strip() for p in pwds if p.strip()]
            if pwds:
                engine.train(pwds)
                print(f"Trained on {len(pwds)} passwords")

        elif choice == "8":
            print("\n--- 10 EXTREME Passwords ---")
            for i in range(10):
                print(f"{i+1}. {engine.generate_extreme(14)}")

        elif choice == "0":
            print("Stay secure!")
            break

if __name__ == "__main__":
    main()

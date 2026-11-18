"""
SAFE TOOLS - 100% offline, no admin, no internet, no other people's data
Run: python safe_tools.py
"""

import os
import csv
import json
import shutil
import random
import string
import datetime

# ---------- 1. SAFE FILE ORGANIZER ----------
def organize_folder():
    folder = input("\nEnter folder to organize (press Enter for Downloads): ").strip()
    if not folder:
        folder = os.path.join(os.path.expanduser("~"), "Downloads")

    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        return

    # Only these safe categories - it will NEVER touch .exe system files or hidden files
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".webp", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".csv", ".xlsx"],
        "Videos": [".mp4", ".mov", ".mkv"],
        "Music": [".mp3", ".wav"],
        "Archives": [".zip", ".rar"],
    }

    moved = 0
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if not os.path.isfile(file_path):
            continue
        if filename.startswith("."):  # skip hidden/system files
            continue

        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        for category, extensions in categories.items():
            if ext in extensions:
                dest_folder = os.path.join(folder, category)
                os.makedirs(dest_folder, exist_ok=True)
                # Don't overwrite if file already exists
                dest_path = os.path.join(dest_folder, filename)
                if os.path.exists(dest_path):
                    name, ext2 = os.path.splitext(filename)
                    filename = f"{name}_{datetime.datetime.now().strftime('%H%M%S')}{ext2}"
                    dest_path = os.path.join(dest_folder, filename)
                shutil.move(file_path, dest_path)
                moved += 1
                break

    print(f"Done! Moved {moved} files. Nothing was deleted.")

# ---------- 2. SAFE FILE CONVERTER (CSV <-> JSON) ----------
def convert_csv_to_json():
    input_file = input("\nEnter CSV file path: ").strip()
    if not os.path.exists(input_file):
        print("File not found.")
        return

    output_file = input("Enter output JSON file name (e.g. output.json): ").strip()
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)

        print(f"Success! Converted {len(rows)} rows to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def convert_json_to_csv():
    input_file = input("\nEnter JSON file path: ").strip()
    if not os.path.exists(input_file):
        print("File not found.")
        return

    output_file = input("Enter output CSV file name (e.g. output.csv): ").strip()
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data:
            print("JSON file is empty.")
            return

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        print(f"Success! Converted {len(data)} rows to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

# ---------- 3. SAFE PASSWORD GENERATOR (OFFLINE) ----------
def make_password():
    try:
        length = int(input("\nPassword length (12-32, default 16): ") or 16)
        length = max(12, min(32, length))
    except ValueError:
        length = 16

    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = "".join(random.choice(chars) for _ in range(length))
    print(f"\nYour strong password: {password}")
    print("Tip: Save it in your notes / password manager. This code never sends it anywhere.")

# ---------- MENU ----------
def main():
    while True:
        print("\n===== SAFE PYTHON TOOLS =====")
        print("1. Organize a folder (safe, no delete)")
        print("2. Convert CSV -> JSON")
        print("3. Convert JSON -> CSV")
        print("4. Generate strong password (offline)")
        print("5. Exit")

        choice = input("Choose 1-5: ").strip()

        if choice == "1":
            organize_folder()
        elif choice == "2":
            convert_csv_to_json()
        elif choice == "3":
            convert_json_to_csv()
        elif choice == "4":
            make_password()
        elif choice == "5":
            print("Bye! Stay safe.")
            break
        else:
            print("Invalid choice, try 1-5.")

if __name__ == "__main__":
    main()
    
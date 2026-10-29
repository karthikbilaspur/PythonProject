# A simple Python tool to find all anagrams of a given word, with both CLI and GUI support. Includes a fast dictionary-based implementation that avoids brute-force permutation explosion

Features
Two modes: CLI and Tkinter GUI
Length filtering: Set min/max length for anagrams
Dictionary filtering: Use a word list (e.g., words.txt) to only show real words
Fast algorithm: When a dictionary is provided, it uses collections.Counter to check if a word can be built from the input letters — no millions of permutations
Handles duplicates and spaces correctly

Installation
Clone or download this repo
Python 3.8+ required (Tkinter comes with Python on Windows/Mac)
No external dependencies needed
python anagram_gui.py
For dictionary mode, you need a word list file (one word per line):

Download an English word list, e.g.:

https://github.com/dwyl/english-words/blob/master/words_alpha.txt
Save as words.txt in the project folder.

Usage
GUI Version
python anagram_gui.py
Enter a word (e.g., listen)
Set Min length (default 1) and Max length (optional, defaults to word length)
(Optional) Browse and select dictionary file words.txt
Click Find Anagrams
CLI Version
python anagram_cli.py
Or import as a module:

from anagram import find_anagrams_fast, load_dictionary
Without dictionary - generates all permutations (only for short words < 9 letters)
result = find_anagrams_fast("abc", min_length=2, max_length=3)
print(result)  # {'ab', 'ac', 'ba', 'bc', 'ca', 'cb', 'abc', ...}
 With dictionary - FAST, recommended
dict_words = load_dictionary("words.txt")
result = find_anagrams_fast("listen", dict_words=dict_words)
print(result)  # {'listen', 'silent', 'enlist', 'inlets', ...}
API
find_anagrams_fast(
    word: str,
    min_length: int = 1,
    max_length: int | None = None,
    dict_words: set[str] | None = None
) -> set[str]
load_dictionary(file_path: str) -> set[str]
Performance Note
Output:

arm, arms, art, arts, mat, mats, ram, rat, rats, star, stream, master, ...
License
MIT - feel free to use and modify.

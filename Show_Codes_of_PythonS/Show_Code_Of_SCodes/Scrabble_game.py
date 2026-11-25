import tkinter as tk
from typing import List
from tkinter import Entry
import nltk
from nltk.corpus.reader.wordlist import WordListCorpusReader
from nltk.data import find
from PyDictionary import PyDictionary

nltk.download('words')
word_list = set(WordListCorpusReader(find('corpora/words'), 'en').words:())
    def __init__(self):
        self.player_names: List[Entry] = []
        self.score_list = {
    def __init__(self):
        self.score_list = {
            'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2,
            'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
            'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1,
            'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
        }
        self.dictionary: PyDictionary = PyDictionary()
        self.players = {}
        self.current_player = 0
        self.game_over = False
        self.root = tk.Tk()
        self.root.title("Scrabble Game")
        self.player_count_label = tk.Label(self.root, text="Enter number of players:")
        self.player_count_label.pack()
        self.player_count_entry = tk.Entry(self.root)
        self.player_count_entry.pack()
        self.player_count_button = tk.Button(self.root, text="Submit", command=self.get_player_count)
        self.player_count_button.pack()

    def get_player_count(self):
        count = int(self.player_count_entry.get())
        self.player_count_label.pack_forget()
        self.player_count_entry.pack_forget()
        self.player_count_button.pack_forget()
        self.player_names = []
        for i in range(count):
            label = tk.Label(self.root, text=f"Player {i+1}:")
            label.pack()
            entry = tk.Entry(self.root)
            entry.pack()
            self.player_names.append(entry)
        self.submit_names_button = tk.Button(self.root, text="Submit", command=self.start_game)
        self.submit_names_button.pack()

    def start_game(self):
        for entry in self.player_names:
            self.players[entry.get()] = 0
        self.player_count = len(self.players)
        self.player_name_label = tk.Label(self.root, text=list(self.players.keys())[self.current_player])
        self.player_name_label.pack()
        self.word_label = tk.Label(self.root, text="Enter a word:")
        self.word_label.pack()
        self.word_entry = tk.Entry(self.root)
        self.word_entry.pack()
        self.score_button = tk.Button(self.root, text="Submit word", command=self.get_word)
        self.score_button.pack()
        self.definition_button = tk.Button(self.root, text="View definition", command=self.view_definition)
        self.definition_button.pack()
        self.score_label = tk.Label(self.root, text="Scores:")
        self.score_label.pack()
        self.score_text = tk.Text(self.root, height=5, width=20)
        self.score_text.pack()
        self.update_scores()
        for widget in self.root.wkids():
            if widget not in [self.player_name_label, self.word_label, self.word_entry, self.score_button, self.definition_button, self.score_label, self.score_text]:
                widget.pack_forget()

    def valid(self, word):
        return word.lower() in word_list

    def compute_score(self, word):
        word = word.lower()
        if not word.isalpha():
            raise ValueError("Word should only contain alphabetic characters")
        if not self.valid(word):
            raise ValueError("Invalid word")
        return sum(self.score_list[char] for char in word)

    def get_word(self):
        if self.game_over:
            return
        word = self.word_entry.get()
        try:
            score = self.compute_score(word)
            player_name = list(self.players.keys())[self.current_player]
            self.players[player_name] += score
            self.current_player = (self.current_player + 1) % self.player_count
            self.player_name_label['text'] = list(self.players.keys())[self.current_player]
            self.word_entry.delete(0, tk.END)
            self.update_scores()
            if self.current_player == 0:
                self.check_game_over()
        except ValueError as e:
            print(str(e))

    def view_definition(self):
        word = self.word_entry.get()
        if word:
            definition = self.dictionary.meaning(word)
            if definition:
                definition_window = tk.Toplevel(self.root)
                definition_window.title(f"Definition of {word}")
                definition_text = tk.Text(definition_window, height=10, width=40)
                definition_text.pack()
                definition_text.insert(tk.END, str(definition))
                definition_text.config(state="disabled")
            else:
                print("Word not found in dictionary")
        else:
            print("Please enter a word")

    def update_scores(self):
        self.score_text.delete('1.0', tk.END)
        for player, score in self.players.items():
            self.score_text.insert(tk.END, f"{player}: {score}\n")

    def check_game_over(self):
        # Simple game over condition: each player has played 5 rounds
        if list(self.players.values()).count(0) == 0:
            self.game_over = True
            self.player_name_label['text'] = "Game Over!"
            self.word_label['text'] = ""
            self.word_entry.pack_forget()
            self.score_button.pack_forget()
            self.definition_button.pack_forget()
            winner = max(self.players, key=self.players.get)
            self.score_text.delete('1.0', tk.END)
            self.score_text.insert(tk.END, f"Winner: {winner}\n")
            self.update_scores()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = ScrabbleGame()
    game.run()
import requests
import tkinter as tk
from tkinter import messagebox

class GitHubSearch:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitHub Repository Search")

        self.owner_label = tk.Label(self.root, text="Repository Owner:")
        self.owner_label.pack()
        self.owner_entry = tk.Entry(self.root)
        self.owner_entry.pack()

        self.repo_label = tk.Label(self.root, text="Repository Name:")
        self.repo_label.pack()
        self.repo_entry = tk.Entry(self.root)
        self.repo_entry.pack()

        self.keyword_label = tk.Label(self.root, text="Search Keyword:")
        self.keyword_label.pack()
        self.keyword_entry = tk.Entry(self.root)
        self.keyword_entry.pack()

        self.search_button = tk.Button(self.root, text="Search", command=self.search)
        self.search_button.pack()

        self.result_text = tk.Text(self.root, height=10, width=50)
        self.result_text.pack()

    def get_repository_contents(self, repo_owner: str, repo_name: str) -> list[dict[str, str | int | bool | None]] | None:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            messagebox.showerror("Error", f"Failed to fetch repository contents. Status code: {response.status_code}")
            return None

    def filter_items_by_keyword(self, contents: list[dict[str, object]], keyword: str, repo_owner: str, repo_name: str) -> list[tuple[str, str]]:
        filtered_items = []
        repo_url = f"https://github.com/{repo_owner}/{repo_name}"

        for item in contents:
            item_name = item["name"].lower()
            item_type = item["type"]

            if keyword.lower() in item_name:
                if item_type == "file":
                    filtered_items.append((item_name, item["html_url"]))
                elif item_type == "dir":
                    filtered_items.append((item_name, item["html_url"]))

        return filtered_items

    def search(self):
        repo_owner = self.owner_entry.get()
        repo_name = self.repo_entry.get()
        keyword = self.keyword_entry.get()

        contents = self.get_repository_contents(repo_owner, repo_name)

        if contents:
            found_items = self.filter_items_by_keyword(contents, keyword, repo_owner, repo_name)

            if found_items:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Found items matching the keyword:\n")
                for idx, (item_name, item_url) in enumerate(found_items, start=1):
                    self.result_text.insert(tk.END, f"{idx}) {item_name} ({item_url})\n")
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "No items found matching the keyword.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    search = GitHubSearch()
    search.run()
import os
import tkinter as tk
from tkinter import messagebox
from typing import Any, cast

import requests

HEADERS = {"User-Agent": "GitHubSearch demo/1.0", "Accept": "application/vnd.github+json"}
TOKEN = os.environ.get("GITHUB_TOKEN")
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


class GitHubSearch:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitHub Repository Search")
        self.root.geometry("520x420")
        for label in ["Repository Owner:", "Repository Name:", "Search Keyword:"]:
            tk.Label(self.root, text=label).pack(pady=(8, 0))
            entry = tk.Entry(self.root, width=45)
            entry.pack()
            setattr(self, label.split()[1].lower() + "_entry",
                    entry)  # owner_entry / repo_entry / keyword_entry — see below
        # The loop above is fragile, so re-bind explicitly:
        # (entries were created in order: owner, repo, keyword)
        children = [w for w in self.root.winfo_children() if isinstance(w, tk.Entry)]
        self.owner_entry, self.repo_entry, self.keyword_entry = children
        tk.Button(self.root, text="Search (recursive)", command=self.search).pack(pady=10)
        self.result_text = tk.Text(self.root, height=14, width=60)
        self.result_text.pack(padx=10, pady=5)

    def _get(self, url: str):
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 404:
            raise ValueError("Repo not found (or private). Check owner/name.")
        if resp.status_code == 403:
            raise ValueError("GitHub rate limit hit. Set GITHUB_TOKEN env var and retry.")
        resp.raise_for_status()
        return resp.json()

    def _walk(self, owner: str, repo: str, path: str = "") -> list[dict[str, Any]]:
        """Recursively list all files via /contents API (top-level + subdirs)."""
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        items = self._get(url)
        if isinstance(items, dict):  # single file returned
            return [items]
        out: list[dict[str, Any]] = []
        for item in items:
            if item["type"] == "dir":
                out.extend(self._walk(owner, repo, item["path"]))
            else:
                out.append(item)
        return out

    def search(self):
        owner = self.owner_entry.get().strip()
        repo = self.repo_entry.get().strip()
        keyword = self.keyword_entry.get().strip().lower()
        if not owner or not repo or not keyword:
            messagebox.showerror("Invalid Input", "Fill in owner, repo, and keyword.")
            return
        try:
            contents = self._walk(owner, repo)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        found = [(i["path"], i["html_url"]) for i in contents if keyword in i["name"].lower()]
        self.result_text.delete("1.0", tk.END)
        if not found:
            self.result_text.insert(tk.END, "No items found matching the keyword.")
            return
        self.result_text.insert(tk.END, f"Found {len(found)} item(s):\n")
        for idx, (path, url) in enumerate(found, 1):
            self.result_text.insert(tk.END, f"{idx}) {path} ({url})\n")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    GitHubSearch().run()

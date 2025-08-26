import requests
import json
from datetime import datetime

class GitHubAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/json"
        }

    def get_user_contributions(self, username):
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_contributors(self, repo_owner, repo_name):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contributors"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_repo_info(self, repo_owner, repo_name):
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

    def get_user_repos(self, username):
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

def main():
    token = "YOUR_GITHUB_TOKEN"
    github_api = GitHubAPI(token)

    while True:
        print("\nGitHub API Menu:")
        print("1. Get User Contributions")
        print("2. Get Contributors")
        print("3. Get Repository Info")
        print("4. Get User Repositories")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter the GitHub username: ")
            user_contributions = github_api.get_user_contributions(username)
            if user_contributions:
                print("User Contributions:")
                print(json.dumps(user_contributions, indent=4))
        elif choice == "2":
            repo_owner = input("Enter the repository owner: ")
            repo_name = input("Enter the repository name: ")
            contributors = github_api.get_contributors(repo_owner, repo_name)
            if contributors:
                print("Contributors:")
                for contributor in contributors:
                    print(contributor["login"])
        elif choice == "3":
            repo_owner = input("Enter the repository owner: ")
            repo_name = input("Enter the repository name: ")
            repo_info = github_api.get_repo_info(repo_owner, repo_name)
            if repo_info:
                print("Repository Info:")
                print(json.dumps(repo_info, indent=4))
        elif choice == "4":
            username = input("Enter the GitHub username: ")
            user_repos = github_api.get_user_repos(username)
            if user_repos:
                print("User Repositories:")
                for repo in user_repos:
                    print(repo["name"])
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
import requests
import sys
from github import Github

def repository_names(user):
    return [repo for repo in user.get_repos()]

def repository_details(user):
    repo_details = []
    for repo in repository_names(user):
        details = {
            "Name": repo.full_name.split("/")[1],
            "Description": repo.description if repo.description else "No description",
            "Created on": repo.created_at,
            "Programming language": repo.language if repo.language else "Not specified",
            "Forked": f"{repo.forks} time(s)",
            "Stars": repo.stargazers_count,
            "Watchers": repo.watchers_count,
            "URL": repo.html_url
        }
        repo_details.append(details)
    return repo_details

def print_repository_details(repo_details):
    for repo in repo_details:
        for title, description in repo.items():
            print(f"{title}: {description}")
        print("\n" + "-" * 120 + "\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script_name.py <github_username>")
        sys.exit(1)

    username = sys.argv[1]
    g = Github()
    try:
        user = g.get_user(username)
        repo_details = repository_details(user)
        print_repository_details(repo_details)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

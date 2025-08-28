import os
import requests
import json
from github import Github
import argparse

# GitHub credentials
GITHUB_TOKEN = "your_github_token"
GITHUB_USERNAME = "your_github_username"

# Create a GitHub instance
g = Github(GITHUB_TOKEN)

def create_repository(repo_name, private=False, description=""):
    try:
        # Create a new repository
        repo = g.get_user().create_repo(repo_name, private=private, description=description)
        print(f"Repository '{repo_name}' created successfully!")
        return repo
    except Exception as e:
        print(f"Error creating repository: {e}")

def initialize_local_repo(repo_name):
    try:
        # Initialize a local repository
        os.mkdir(repo_name)
        os.chdir(repo_name)
        os.system("git init")
        print(f"Local repository '{repo_name}' initialized successfully!")
    except Exception as e:
        print(f"Error initializing local repository: {e}")

def add_files(repo_name, files):
    try:
        # Create new files
        for file in files:
            with open(file, "w") as f:
                f.write(f"# {repo_name} - {file}")
        os.system("git add .")
        print(f"Files added to repository '{repo_name}' successfully!")
    except Exception as e:
        print(f"Error adding files: {e}")

def commit_changes(repo_name, message):
    try:
        # Commit changes
        os.system(f"git commit -m '{message}'")
        print(f"Changes committed to repository '{repo_name}' successfully!")
    except Exception as e:
        print(f"Error committing changes: {e}")

def push_changes(repo_name):
    try:
        # Push changes to remote repository
        os.system(f"git remote add origin https://github.com/{GITHUB_USERNAME}/{repo_name}.git")
        os.system("git push -u origin master")
        print(f"Changes pushed to repository '{repo_name}' successfully!")
    except Exception as e:
        print(f"Error pushing changes: {e}")

def main():
    parser = argparse.ArgumentParser(description="GitHub Automation Script")
    parser.add_argument("-n", "--name", help="Repository name", required=True)
    parser.add_argument("-p", "--private", action="store_true", help="Create private repository")
    parser.add_argument("-d", "--description", help="Repository description")
    parser.add_argument("-f", "--files", nargs="+", help="Files to add to repository")
    parser.add_argument("-m", "--message", help="Commit message", default="Initial commit")
    args = parser.parse_args()

    repo = create_repository(args.name, args.private, args.description)
    initialize_local_repo(args.name)
    if args.files:
        add_files(args.name, args.files)
    else:
        add_files(args.name, ["README.md"])
    commit_changes(args.name, args.message)
    push_changes(args.name)

if __name__ == "__main__":
    main()